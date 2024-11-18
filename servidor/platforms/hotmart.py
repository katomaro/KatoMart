from ..models.configs import Configuration
from ..models.courses import PlatformAuth, Platform, Course, Module, Lesson, File
from sqlalchemy.orm import joinedload

from .base import PlatformScraper
from ..scrappers.requests_based import RequestsScraper
from ..scrappers.selenium_based import SeleniumScraper
from ..scrappers.utils import clone_session
import time
import datetime
import pathlib

from ..downloaders.Downloader import Downloader

from general_utils import sanitize_path_component
from bs4 import BeautifulSoup
import json
import m3u8
import tempfile
import os

class HotmartScraper(PlatformScraper):
    LOGIN_URL = 'https://consumer.hotmart.com/login'  # kind: LOGIN
    PRODUCTS_URLS = ['https://api-hub.cb.hotmart.com/club-drive-api/rest/v2/purchase/?archived=UNARCHIVED', 
                     'https://api-hub.cb.hotmart.com/club-drive-api/rest/v1/purchase/free/?archived=UNARCHIVED']  # kind: PRODUCT_LIST
    USER_RESOURCES = 'https://api-club-user.cb.hotmart.com/v4/users/resources'  # kind: PRODUCT_INFORMATION
    CHECK_CLUB_REDIRECT_URL = 'https://api-content-platform-space-gateway.cp.hotmart.com/rest/public/v1/products/{product_id}/info-management?productId={product_id}'  # kind: PRODUCT_INFORMATION
    # "content":{"shouldRedirectToClub":false}
    # if true, then
    NEW_MEMBER_AREA_URL = 'https://api-club-course-consumption-gateway.hotmart.com/v1/navigation'  # kind: PRODUCT_CONTENT 
    NEW_LESSON_URL = 'https://api-content-platform-space-gateway.cp.hotmart.com/rest/public/v1/memberships/products/{product_id}?productId={product_id}'  # kind: PRODUCT_CONTENT
    # widevine url a["{\"msg\":\"result\",\"id\":\"13\",\"result\":{\"url\":\"https://api-club.cb.hotmart.com/rest/v3/userarea/code\",\"status\":200,\"content\":\"uuidv4\"}}"]
    # if false, then
    # widevine url remains the same
    # needs 'Club' header
    MEMBER_AREA_URL = 'https://api-club.cb.hotmart.com/rest/v3/navigation'  # kind: PRODUCT_CONTENT
    LESSON_URL = 'https://api-club.cb.hotmart.com/rest/v3/page/{page_hash}?pageHash={page_hash}'  # kind: LESSON_CONTENT

    def __init__(self, auth_data, session, course_id=None):
        super().__init__(auth_data)
        self.scraper = RequestsScraper()
        self.session = session
        self.user_id = auth_data.id
        self.auth_token = auth_data.token
        self.token_expires_at = auth_data.token_expires_at
        self.refresh_token = auth_data.refresh_token
        self.course_id = course_id
    
    #  OVERRIDES
    def add_to_normal_queue(self, lesson_info):
        """Add a lesson to the normal download queue."""
        self.normal_queue.append(lesson_info)

    def add_to_priority_queue(self, lesson_info):
        """Add a lesson to the priority download queue."""
        self.priority_queue.append(lesson_info)
        self.remove_from_normal_queue(lesson_info)

    def remove_from_normal_queue(self, lesson_info):
        """Remove a lesson from the normal queue."""
        self.normal_queue = [item for item in self.normal_queue if not self.compare_lesson_info(item, lesson_info)]

    def remove_from_priority_queue(self, lesson_info):
        """Remove a lesson from the priority queue."""
        self.priority_queue = [item for item in self.priority_queue if not self.compare_lesson_info(item, lesson_info)]

    def demote_from_priority_queue(self, lesson_info):
        """
        Remove a lesson from the priority queue and add it back to the normal queue.
        """
        self.remove_from_priority_queue(lesson_info)
        self.add_to_normal_queue(lesson_info)

    def compare_lesson_info(self, item1, item2):
        """
        Helper method to compare two lesson_info dictionaries.
        """
        return item1.get('lesson')['lesson_id'] == item2.get('lesson')['lesson_id']

    
    def login(self):
        current_time = int(time.time())
        if not self.auth_token or (self.token_expires_at and current_time >= self.token_expires_at):
            bypass_sso = SeleniumScraper()
            bypass_sso.get(self.LOGIN_URL)
            bypass_sso.attempt_cookie_popup('/div/div/div/div[3]/button[2]')
            bypass_sso.login_static_form(
                self.LOGIN_URL,
                self.auth_data.username,
                self.auth_data.password,
                '//*[@id="username"]',
                '//*[@id="password"]',
                '/html/body/main/div/div[1]/div/div[1]/form[1]/div/div/div[4]/button'
            )
            time.sleep(5)
            cookies = bypass_sso.get_cookies()
            # local_storage = bypass_sso.get_local_storage()
            # if local_storage and "cas-js:user" in local_storage:
            #     cas_js_user = json.loads(local_storage["cas-js:user"])
            #     id_token = cas_js_user.get("id_token")
            # print('*'*50)
            # print(auth)
            # print('*'*50)
            user = self.session.query(PlatformAuth).filter_by(id=self.user_id).first()
            self.auth_token = cookies.get('hmVlcIntegration')
            # print('*'*50)
            # print(self.auth_token)
            # print('*'*50)
            self.token_expires_at = int(cookies.get('hmSsoExp').split('|', 1)[0])
            if user:
                user.token = cookies.get('hmVlcIntegration')
                user.token_expires_at = cookies.get('hmSsoExp').split('|', 1)[0]
                user.total_products = 0
                user.is_logged_in = True
                user.valid_combination = True

                self.session.commit()

            self.scraper.session.cookies.update(cookies)
            bypass_sso.close()

        self.scraper.session.headers.update({
            'Authorization': f'Bearer {self.auth_token}'
        })

    def get_course_data(self):
        """
        Fetch the course data using the authenticated session.
        """
        self.login()

        products = []

        for url in self.PRODUCTS_URLS:
            response = self.scraper.get(url)

            if response.status_code != 200:
                raise Exception(f'Error accessing {response.url}: Status Code {response.status_code}')

            data = response.json()

            for product in data.get('data', []):
                products.append(product)
        
        # print('*'*50)
        # print(products)
        # print('*'*50)

        RESOURCES = self.scraper.session.get(self.USER_RESOURCES)
        # print('*'*50)
        # print(RESOURCES.json())
        # print('*'*50)

        res = RESOURCES.json()
        res_mapping = {item['resource']['productId']: item for item in res}

        
        for product in products:
            course_id = product.get('product', {}).get('id', '(Curso sem ID)')
            platform_id = self.auth_data.platform_id

            existing_course = self.session.query(Course).filter_by(id=course_id, platform_id=platform_id).first()
            if not existing_course:
                pp = Course(
                    id=product.get('product', {}).get('id', '(Curso sem ID)'),
                    name=product.get('product', {}).get('name', '(Curso com nome desconhecido)'),
                    formatted_name=sanitize_path_component(product.get('product', {}).get('name', '(Curso com nome desconhecido)')),
                    extra_data = res_mapping.get(course_id, {}),
                    teacher=product.get('product', {}).get('seller', {}).get('name', '(Professor Desconhecido)'),
                    description=product.get('product', {}).get('descrption', '(Descrição não disponível)'),
                    platform_id=self.auth_data.platform_id,
                    platform_auth_id=self.user_id
                )
                self.session.add(pp)
            self.session.commit()
        user = self.session.query(PlatformAuth).filter_by(id=self.user_id).first()
        if user:
            user.total_products = len(products)
            self.session.commit()
        

    def get_product_information(self, product_id):
        """
        Fetch detailed product information.
        """
        self.login()

        desired_course = self.session.query(Course).filter_by(katomart_id=product_id).first()
        if not desired_course:
            raise Exception(f'Course with ID {product_id} not found.')
        desired_course = desired_course.to_dict()

        RESOURCES = self.scraper.session.get(self.USER_RESOURCES)  # Retorna os cursos do usuario em um array de dicionarios
        # print('*'*50)
        # print(RESOURCES.json())
        # print('*'*50)
        #         {
        #     "resource":{
        #         "role":"STUDENT",
        #         "status":"ACTIVE",
        #         "userAreaId":INTEGER,
        #         "productId":INTEGER,
        #         "subdomain":"STRING"
        #     },
        #     "roles":[
        #         "STUDENT"
        #     ]
        # },
        course_information = None
        for resource in RESOURCES.json():
            if int(resource.get('resource', {}).get('productId')) == int(desired_course.get('id')):
                course_information = resource
                break

        USE_NEW_URL = self.scraper.session.get(self.CHECK_CLUB_REDIRECT_URL.format(product_id=desired_course.get('id')))
        # print('*'*50)
        # print(USE_NEW_URL)
        # print(USE_NEW_URL.json())  # {'shouldRedirectToClub': False}
        # print('*'*50)
        USE_NEW = USE_NEW_URL.json().get('shouldRedirectToClub', False)

        course_club = course_information.get('resource', {}).get('subdomain')

        if not USE_NEW:
            self.scraper.session.headers.update({
                'Club': course_information.get('resource', {}).get('subdomain')
            })
        # self.scraper.session.headers.update({
        #     'club': product_subdomain
        # })

        course_data = None

        if not USE_NEW:
            course_data = self.scraper.session.get(self.MEMBER_AREA_URL)
        else:
            course_data = self.scraper.session.get(self.NEW_MEMBER_AREA_URL)

        product_info = course_data.json()  # Modulos em um dicionario cuja chave "modules" eh um array com os modulos, aulas na chave pages, widevine na chave code

        sorted_modules = sorted(product_info["modules"], key=lambda x: x["moduleOrder"])
        for i, module in enumerate(sorted_modules, start=1):
            module["moduleOrder"] = i
            sorted_pages = sorted(module["pages"], key=lambda x: x["pageOrder"])
            for j, page in enumerate(sorted_pages, start=1):
                page["pageOrder"] = j
            module["pages"] = sorted_pages

        product_info["modules"] = sorted_modules
        # print('*'*100)
        # print(product_info)
        # print('*'*100)

        for module_data in product_info.get('modules', []):
            self.save_module(module_data, desired_course.get('id'))
            module_id = module_data['id']

            for lesson_data in module_data["pages"]:
                self.save_lesson(lesson_data, module_id)
                lesson_id = lesson_data['hash']

    def get_all_downloadable_content(self):
        pass
    
    def get_lesson_information(self, lesson_hash):
        """
        Fetch detailed lesson information.
        """
        self.login()

        lesson_data = self.scraper.session.get(self.LESSON_URL.format(page_hash=lesson_hash)).json()
        # print('*'*50)
        # print('*'*50)
        # print('*'*50)
        # print(lesson_data)
        # print('*'*50)
        # print('*'*50)
        # print('*'*50)
        lesson_description = lesson_data.get('content', 'Descrição não disponível')
        has_media = bool(lesson_data.get('mediasSrc', []))
        if has_media:
            for media_index, media in enumerate(lesson_data.get('mediasSrc', []), start=1):
                id = media.get('mediaCode', 'ID não disponível')
                name = media.get('mediaName', 'Nome não disponível')
                formatted_name = sanitize_path_component(name)
                file_size = media.get('mediaSize', 0)
                file_type = media.get('mediaType', 'Desconhecido')
                file_data = {
                    'id': id,
                    'name': name,
                    'formatted_name': formatted_name,
                    'order': media_index,
                    'file_size': file_size,
                    'file_type': file_type,
                    'urls': {'url1': media.get('mediaSrcUrl'), 'url2': media.get('mediaSrcUrlLegacy')}
                }
                self.save_file(file_data, lesson_hash)

        return lesson_description
        
    
    def save_module(self, module_data, course_id):
        existing_module = self.session.query(Module).filter_by(id=module_data['id'], course_id=course_id).first()
        
        if existing_module:
            existing_module.extra_data = {"code": module_data['code'], "extra": module_data['extra']},
            existing_module.locked = module_data['locked']
            existing_module.name = module_data['name']
            existing_module.order = module_data['moduleOrder']
            existing_module.updated_at = int(datetime.datetime.now().timestamp())
        else:
            new_module = Module(
                id=module_data['id'],
                extra_data = {"code": module_data['code'], "extra": module_data['extra']}, 
                name=module_data['name'],
                formatted_name=sanitize_path_component(module_data['name']),
                is_locked=module_data['locked'],
                order=module_data['moduleOrder'],
                course_id=course_id,
                created_at=int(datetime.datetime.now().timestamp()),
                updated_at=int(datetime.datetime.now().timestamp())
            )
            self.session.add(new_module)
        
        self.session.commit()

    def save_lesson(self, lesson_data, module_id):
        existing_lesson = self.session.query(Lesson).filter_by(id=lesson_data['hash'], module_id=module_id).first()
        
        if existing_lesson:
            existing_lesson.extra_data = {'completed': lesson_data['completed']}
            existing_lesson.name = lesson_data['name']
            existing_lesson.locked = lesson_data['locked']
            existing_lesson.order = lesson_data['pageOrder']
            existing_lesson.updated_at = int(datetime.datetime.now().timestamp())
        else:
            new_lesson = Lesson(
                id=lesson_data['hash'],
                extra_data={'completed': lesson_data['completed']},
                name=lesson_data['name'],
                is_locked=lesson_data['locked'],
                formatted_name=sanitize_path_component(lesson_data['name']),
                order=lesson_data['pageOrder'],
                module_id=module_id,
                description=self.get_lesson_information(lesson_data['hash']),
                created_at=int(datetime.datetime.now().timestamp()),
                updated_at=int(datetime.datetime.now().timestamp())
            )
            self.session.add(new_lesson)
        
        self.session.commit()
    
    def save_file(self, file_data, lesson_id):
        existing_file = self.session.query(File).filter_by(id=file_data['id'], lesson_id=lesson_id).first()

        if existing_file:
            existing_file.file_type = file_data['file_type']
            existing_file.order = file_data['order']
            existing_file.file_size = file_data['file_size']
            existing_file.extra_data = {'urls': file_data['urls']}
            existing_file.updated_at = int(datetime.datetime.now().timestamp())
        else:
            new_file = File(
                id=file_data['id'],
                name=file_data['name'],
                formatted_name=file_data['formatted_name'],
                file_type=file_data['file_type'],
                order=file_data['order'],
                file_size=file_data['file_size'],
                lesson_id=lesson_id,
                extra_data={'urls': file_data['urls']},
                created_at=int(datetime.datetime.now().timestamp()),
                updated_at=int(datetime.datetime.now().timestamp())
            )
            self.session.add(new_file)

        self.session.commit()

    def get_course_hierarchy(self, course_id):
        course = self.session.query(Course).options(
            joinedload(Course.modules)
            .joinedload(Module.lessons)
            .joinedload(Lesson.files)
        ).filter(Course.katomart_id == course_id).first()
        
        if not course:
            raise Exception(f'Course with katomart_id {course_id} not found.')
        
        return course

    def build_course_structure(self, course):
        course_structure = {
            'course_id': course.katomart_id,
            'course_name': course.name,
            'formatted_name': course.formatted_name,
            'modules': []
        }
        
        for module in course.modules:
            module_dict = {
                'module_id': module.katomart_id,
                'module_name': module.name,
                'formatted_name': module.formatted_name,
                'lessons': []
            }
            
            for lesson in module.lessons:
                lesson_dict = {
                    'lesson_id': lesson.katomart_id,
                    'lesson_name': lesson.name,
                    'formatted_name': lesson.formatted_name,
                    'files': []
                }
                
                for file in lesson.files:
                    file_dict = {
                        'file_id': file.katomart_id,
                        'file_name': file.name,
                        'formatted_name': file.formatted_name,
                        'file_type': file.file_type,
                        'file_size': file.file_size,
                        'urls': file.extra_data.get('urls')
                    }
                    lesson_dict['files'].append(file_dict)
                
                module_dict['lessons'].append(lesson_dict)
            
            course_structure['modules'].append(module_dict)
        
        return course_structure

    def start_downloads(self):
        """
        Start processing the download queues.

        This method processes the priority queue first. After every lesson download, it checks
        if there is an item in the priority queue and downloads it before continuing with the normal queue.
        """
        course = self.get_course_hierarchy(self.course_id)
        course_structure = self.build_course_structure(course)
        download_path = pathlib.Path(self.session.query(Configuration).filter_by(key='dl_storage_path').first().value)
        course_club = course.extra_data.get('resource').get('subdomain')

        # Build the queue of lessons
        for module_index, module in enumerate(course_structure['modules'], start=1):
            for lesson_index, lesson in enumerate(module['lessons'], start=1):
                # Build the lesson download path
                module_download_path = download_path / course_structure['formatted_name'] / f"{module_index:02d}. {module['formatted_name']}"
                lesson_download_path = module_download_path / f"{lesson_index:02d}. {lesson['formatted_name']}"
                # Enqueue the lesson
                lesson_info = {
                    'module_index': module_index,
                    'lesson_index': lesson_index,
                    'module': module,
                    'lesson': lesson,
                    'lesson_download_path': lesson_download_path,
                    'course_club': course_club
                }
                self.add_to_normal_queue(lesson_info)

        self.max_progress = len(self.normal_queue) + len(self.priority_queue)

        print("Starting download process...")
        self.pause()

        while not self.stop_event.is_set():
            if self.pause_event.is_set():
                print("Download paused... Waiting to resume.")
                while self.pause_event.is_set() and not self.stop_event.is_set():
                    time.sleep(1)

            if self.stop_event.is_set():
                break

            # Check priority queue
            if self.priority_queue:
                lesson_info = self.priority_queue.pop(0)
                # Remove from normal queue if it's there
                self.remove_from_normal_queue(lesson_info)
            elif self.normal_queue:
                lesson_info = self.normal_queue.pop(0)
            else:
                break

            try:
                module_index = lesson_info['module_index']
                lesson_index = lesson_info['lesson_index']
                module = lesson_info['module']
                lesson = lesson_info['lesson']
                lesson_download_path = lesson_info['lesson_download_path']
                course_club = lesson_info['course_club']

                print(f"Processing lesson {lesson_index} in module {module_index}: {lesson['formatted_name']}")

                # Process the lesson
                self.process_lesson(lesson, lesson_download_path, course_club)

                # Update lesson status in the database
                self.update_lesson_status(lesson['lesson_id'])
                self.progress += 1

            except Exception as e:
                print(f"Error processing lesson: {e}")
            finally:
                time.sleep(1)

        print("Download process has been stopped.")

    def process_lesson(self, lesson, lesson_download_path, course_club):
        """
        Process a single lesson: create directories, save descriptions, download files.
        """
        lesson_download_path.mkdir(parents=True, exist_ok=True)
        if lesson.get('description'):
            with open(lesson_download_path / 'Descricao.html', 'w', encoding='utf-8') as desc_file:
                desc_file.write(lesson['description'])

        if lesson.get('files'):
            for file_index, file in enumerate(lesson['files'], start=1):
                best_url, file_session = self.construct_media_url(file, course_club)
                file_download_path = lesson_download_path / f"{file_index:02d}. Aula.mp4"

                if not best_url:
                    print(f"Unable to construct media URL for file {file['formatted_name']}")
                    continue

                file_info = {
                    'id': file['file_id'],
                    'best_url': best_url,
                    'down_url': file['urls']['url1'],
                    'destination_path': file_download_path,
                    'extra_data': {'referer': 'https://cf-embed.play.hotmart.com/'}
                }

                url = file_info.get('best_url')
                try:
                    print(f"Starting download for: {url}")
                    downloader = Downloader(db_session=self.session, session=file_session)
                    print('Downloader initiated.')
                    downloader.download_hls_variant_playlist(
                        file_info['best_url'],
                        file_info['destination_path'],
                    )

                    # Update file status in the database
                    self.update_file_status(file_info['id'])
                except Exception as e:
                    print(f"Error downloading {url}: {e}")
                finally:
                    time.sleep(downloader.download_await_time)
        else:
            print(f"No files to download for lesson {lesson['formatted_name']}")

    def update_lesson_status(self, lesson_id):
        """Update the lesson status in the database."""
        lesson_record = self.session.query(Lesson).filter_by(id=lesson_id).first()
        if lesson_record:
            lesson_record.is_downloaded = True
            lesson_record.download_date = int(datetime.datetime.now().timestamp())
            lesson_record.updated_at = int(datetime.datetime.now().timestamp())
            self.session.commit()
            


    def update_file_status(self, file_id):
        """Update the file status in the database."""
        file_record = self.session.query(File).filter_by(id=file_id).first()
        if file_record:
            file_record.is_downloaded = True
            file_record.download_date = int(datetime.datetime.now().timestamp())
            file_record.updated_at = int(datetime.datetime.now().timestamp())
            self.session.commit()

    def construct_media_url(self, file_data, course_club):
        file_url = file_data.get('urls').get('url1')
        if not file_url:
            file_url = file_data.get('urls').get('url2')
        if not file_url:
            return None
        
        tmp_session = clone_session(self.scraper.session)
        tmp_session.headers.update({
            'Club': course_club,
            'Referer': f'https://{course_club}club.hotmart.com/',
            'Origin': f'https://{course_club}club.hotmart.com'
        })
        
        file_response = tmp_session.get(file_url)

        # print('*'*50)
        # print(file_response.text)
        # print('*'*50)

        soup = BeautifulSoup(file_response.text, 'html.parser')
        script_tag = soup.find('script', {'id': '__NEXT_DATA__'})
        if not script_tag:
            return None
        data = json.loads(script_tag.string)
        application_data = data.get('props', {}).get('pageProps', {}).get('applicationData', {})
        media_has_drm = application_data.get('isDrmEnabled', False)
        is_media_public = application_data.get('isMediaPublic', False)
        needs_jwt = application_data.get('isJwtSignature', False)
        media_type = application_data.get('mediaType', '')
        transmission_type = application_data.get('transmissionType', '')
        media_flags = {}
        flags = application_data.get('flags', {})
        media_flags['ENABLE_PLAYER_V4_ENCRYPTION'] = flags.get('ENABLE_PLAYER_V4_ENCRYPTION', False)
        media_flags['ENABLE_PLAYER_DISPLAY_USER_ID'] = flags.get('ENABLE_PLAYER_DISPLAY_USER_ID', False)  # Fake DRM lmao
        media_flags['ENABLE_PLAYER_V4_API'] = flags.get('ENABLE_PLAYER_V4_API', False)
        media_flags['ENABLE_PLAYER_FINGER_PRINT'] = flags.get('ENABLE_PLAYER_FINGER_PRINT', False)  # DANGEROUS
        media_code = application_data.get('mediaCode', '')
        application_key = application_data.get('applicationKey', '')
        media_membership_id = application_data.get('clubMembershipId', '')
        mux_api_key = application_data.get('muxApiKey', '')
        thumbnail_url = application_data.get('thumbnailUrl', '')
        media_assets = application_data.get('mediaAssets', [])
        finish_transcode_date = application_data.get('finishTranscodeDate', '')
        cdn_provider = application_data.get('cdnProvider', '')
        user_code = application_data.get('userCode', '')
        signature = application_data.get('signature', '')
        api_version = application_data.get('apiVersion', '')  # V5
        platform_user_id = application_data.get('platformUserId', '')
        media_query = application_data.get('query', '')
        media_build_id = application_data.get('buildId', '')
        asset_prefix = application_data.get('assetPrefix', '')
        is_fallback = application_data.get('isFallback', False)

        filtered_html = {}

        filtered_html['media_has_drm'] = media_has_drm
        filtered_html['is_media_public'] = is_media_public
        filtered_html['needs_jwt'] = needs_jwt
        filtered_html['media_type'] = media_type
        filtered_html['transmission_type'] = transmission_type
        filtered_html['media_flags'] = media_flags
        filtered_html['media_code'] = media_code
        filtered_html['application_key'] = application_key
        filtered_html['media_membership_id'] = media_membership_id
        filtered_html['mux_api_key'] = mux_api_key
        filtered_html['thumbnail_url'] = thumbnail_url
        filtered_html['media_assets'] = media_assets
        filtered_html['finish_transcode_date'] = finish_transcode_date
        filtered_html['cdn_provider'] = cdn_provider
        filtered_html['user_code'] = user_code
        filtered_html['signature'] = signature
        filtered_html['api_version'] = api_version
        filtered_html['platform_user_id'] = platform_user_id
        filtered_html['media_query'] = media_query
        filtered_html['media_build_id'] = media_build_id
        filtered_html['asset_prefix'] = asset_prefix
        filtered_html['is_fallback'] = is_fallback

        # Aplicacao completa utiliza estas coisas

        if filtered_html['media_has_drm']:
            return None  # Suportado no aplicativo completo

        media_assets = data['props']['pageProps']['applicationData']['mediaAssets']

        best_quality_asset = max(media_assets, key=lambda x: x.get('height', 0))
        # A aplicacao completa sempre pega o asset de maior qualidade, a outra deixa escolher.
        url = best_quality_asset.get('url')
        master_playlist = tmp_session.get(url)
        master_playlist = m3u8.loads(master_playlist.text)
        sorted_variants = sorted(master_playlist.playlists, key=lambda x: x.stream_info.bandwidth, reverse=True)
        if sorted_variants:
            best_variant = sorted_variants[0]

        url_template = url.rsplit('/hls/', 1)[0] + '/hls/'
        best_playlist = url_template + best_variant.uri
        return best_playlist, tmp_session


    def close(self):
        """
        Close the scraper session.
        """
        self.scraper.close()
