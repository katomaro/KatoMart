import shutil
import os
import re
import threading
import datetime

from flask import jsonify, g, send_from_directory, request, Response, abort, send_file

from .auth import requires_consent

from .models.courses import PlatformAuth, Platform, PlatformURL, Course, Module, Lesson, File, VideoNote, PdfAnnotation
from .models.configs import Configuration

from .database import get_session

from .platforms import get_platform_scraper

from .install import try_auto_install_tp_tool

from uuid import uuid4

import requests

from sqlalchemy.orm import joinedload


scraper_manager = {}
scraper_manager_lock = threading.Lock()


def setup_main_route(main_bp):
    @main_bp.route('/', defaults={'path': ''})
    @main_bp.route('/<path:path>')
    def catch_all(path):
        if path != "" and os.path.exists(main_bp.static_folder + '/' + path):
            return send_from_directory(main_bp.static_folder, path)
        else:
            return send_from_directory(main_bp.static_folder, 'index.html')


def setup_api_routes(api_blueprint):
    TP_IDS = {
        1: 'ffmpeg',
        2: 'geckodriver',
        3: 'bento4'
    }

    @api_blueprint.route('/ping', methods=['GET'])
    def ping():
        return jsonify({
                            "status": "success",
                            "message": "pong",
                            "data": None
                        }), 200

    @api_blueprint.route('/get_katomart_consent', methods=['GET'])
    def get_katomart_consent():
        consent = g.session.query(Configuration).filter_by(key='setup_user_local_consent').first()
        if consent is None:
            return jsonify({
                            "status": "error",
                            "message": "The user hasn't given consent yet.",
                            "data": False
                        }), 404
        if consent.value == "1":
            return jsonify({
                            "status": "success",
                            "message": "The user has given consent.",
                            "data": consent.to_dict()
                        }), 200
        else:
            return jsonify({
                                "status": "error",
                                "message": "The user has not given consent.",
                                "data": consent.to_dict()
                            }), 400
    
    @api_blueprint.route('/set_katomart_consent', methods=['POST'])
    def set_katomart_consent():
        configuration = g.session.query(Configuration).filter_by(key='setup_user_local_consent').first()
        if configuration is None:
            return jsonify({
                            "status": "error",
                            "message": "Configuration key not found.",
                            "data": False
                        }), 404
        data = request.json
        if not data:
            return jsonify({
                            "status": "error",
                            "message": "No data provided.",
                            "data": False
                        }), 400
        for attr, value in data.items():
            setattr(configuration, attr, value)
        g.session.commit()
        return jsonify({
                        "status": "success",
                        "message": "Configuration updated.",
                        "data": configuration.to_dict()
                        }), 200
    
    @api_blueprint.route('/get_all_configurations', methods=['GET'])
    def get_all_configurations():
        all_configurations = g.session.query(Configuration).all()
        if not all_configurations:
            return jsonify({
                            "status": "error",
                            "message": "No configurations found.",
                            "data": False
                        }), 404
        return jsonify({
                            "status": "success",
                            "message": "Fetched all configurations.",
                            "data": [configuration.to_dict() for configuration in all_configurations]
                        }), 200
    
    @api_blueprint.route('/configurations/<string:key>', methods=['GET'])
    @requires_consent
    def get_configuration(key):
        configuration = g.session.query(Configuration).filter_by(key=key).first()
        if configuration is None:
            return jsonify({
                            "status": "error",
                            "message": "Configuration key not found.",
                            "data": False
                        }), 404
        return jsonify({
                            "status": "success",
                            "message": "Configuration fetched.",
                            "data": configuration.to_dict()
                        }), 200

    @api_blueprint.route('/configurations/<string:key>', methods=['POST'])
    @requires_consent
    def update_configuration(key):
        configuration = g.session.query(Configuration).filter_by(key=key).first()
        if configuration is None:
            return jsonify({
                            "status": "error",
                            "message": "Configuration key not found.",
                            "data": False
                        }), 404
        data = request.json
        if not data:
            return jsonify({
                            "status": "error",
                            "message": "No data provided.",
                            "data": False
                        }), 400

        for attr, value in data.items():
            setattr(configuration, attr, value)
        g.session.commit()
        return jsonify({
                        "status": "success",
                        "message": "Configuration updated.",
                        "data": configuration.to_dict()
                        }), 200

    @api_blueprint.route('/check_third_party_tool/<int:id>', methods=['GET'])
    @requires_consent
    def check_third_party_tool(id):
        #tp reads like toilet paper lmao
        has_tool = shutil.which(TP_IDS.get(id))
        if has_tool is None:
            tool = g.session.query(Configuration).filter_by(key=f'install_{TP_IDS.get(id)}').first()
            if not tool['value']:
                return jsonify({
                            "status": "error",
                            "message": f"{TP_IDS.get(id)} not present and not marked for installation!",
                            "data": False
                        }), 404
            else:
                return jsonify({
                            "status": "error",
                            "message": f"{TP_IDS.get(id)} not present but marked for installation!",
                            "data": False
                        }), 401
        return jsonify({
                            "status": "success",
                            "message": f"{TP_IDS.get(id)} is present and should be working fine!",
                            "data": True
                        }), 200

    @api_blueprint.route('/auto_install_third_party_tool/<int:id>', methods=['GET'])
    @requires_consent
    def auto_install_third_party_tool(id):
        user_os = g.session.query(Configuration).filter_by(key='user_os').first()
        if user_os['value'] not in ('linux', 'darwin', 'win32'):
            return jsonify({
                            "status": "error",
                            "message": "Unsupported OS",
                            "data": False
                        }), 404

        if id not in TP_IDS.keys():
            return jsonify({
                            "status": "error",
                            "message": "Invalid tool ID",
                            "data": False
                        }), 404
        
        r = try_auto_install_tp_tool(TP_IDS.get(id))
        if not r:
            return jsonify({
                            "status": "error",
                            "message": f"{TP_IDS.get(id)} installation failed!",
                            "data": False
                        }), 400
        return jsonify({
                            "status": "success",
                            "message": f"{TP_IDS.get(id)} installed successfully!",
                            "data": True
                        }), 200
    
    @api_blueprint.route('/install_third_party_tool', methods=['GET'])
    @requires_consent
    def install_third_party_tool():
        return jsonify({
                            "status": "error",
                            "message": "This endpoint is not implemented yet.",
                            "data": False
                        }), 404

    @api_blueprint.route('/video/<path:filename>')
    @requires_consent
    def serve_video(filename):
        video_path = os.path.join('path_to_your_video_files', filename)
        if not os.path.isfile(video_path):
            abort(404)

        file_size = os.path.getsize(video_path)
        range_header = request.headers.get('Range', None)
        if range_header:
            # Parse the 'Range' header
            byte_range = re.search(r'bytes=(\d+)-(\d*)', range_header)
            if byte_range:
                start = int(byte_range.group(1))
                end = byte_range.group(2)
                end = int(end) if end else file_size - 1
                length = end - start + 1

                # Open file and read the specified byte range
                with open(video_path, 'rb') as f:
                    f.seek(start)
                    data = f.read(length)

                # Create partial response
                response = Response(data,
                                    206,
                                    mimetype='video/mp4',
                                    direct_passthrough=True)
                response.headers.add('Content-Range', f'bytes {start}-{end}/{file_size}')
                response.headers.add('Accept-Ranges', 'bytes')
                response.headers.add('Content-Length', str(length))
            else:
                # Invalid Range header
                abort(400)
        else:
            # Serve the whole file
            return send_file(video_path, mimetype='video/mp4')

        return response

    @api_blueprint.route('/subtitles/<path:filename>')
    @requires_consent
    def serve_subtitles(filename):
        subtitle_path = os.path.join('path_to_your_subtitle_files', filename)
        if not os.path.isfile(subtitle_path):
            abort(404)
        return send_file(subtitle_path, mimetype='text/vtt')

    @api_blueprint.route('/get_all_accounts', methods=['GET'])
    @requires_consent
    def get_all_accounts():
        all_accounts = g.session.query(PlatformAuth).all()
        if all_accounts is None:
            return jsonify({
                            "status": "error",
                            "message": "No accounts found.",
                            "data": False
                        }), 404
        return jsonify({
                            "status": "success",
                            "message": "Fetched all accounts.",
                            "data": [account.to_dict() for account in all_accounts]
                        }), 200
    
    @api_blueprint.route('/save_platform_account', methods=['POST'])
    def save_platform_account():
        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "message": "No data provided.",
                "data": False
            }), 400

        platform_id = data.get('platform_id')
        username = data.get('username')
        password = data.get('password')
        account_domain = data.get('account_domain')
        token = data.get('token')

        if not platform_id or not username or not password:
            return jsonify({
                "status": "error",
                "message": "Fields 'platform_id', 'username', and 'password' are required.",
                "data": False
            }), 400

        # Check if the platform exists
        platform = g.session.query(Platform).filter_by(id=platform_id).first()
        if not platform:
            return jsonify({
                "status": "error",
                "message": f"Platform with id {platform_id} does not exist.",
                "data": False
            }), 404

        # Create a new PlatformAuth instance
        new_auth = PlatformAuth(
            platform_id=platform_id,
            username=username,
            password=password,
            account_domain=account_domain,
            token=token
        )

        try:
            g.session.add(new_auth)
            g.session.commit()

            auth_data = new_auth.to_dict()

            return jsonify({
                "status": "success",
                "message": "Platform account saved successfully.",
                "data": auth_data
            }), 201
        except Exception as e:
            g.session.rollback()
            return jsonify({
                "status": "error",
                "message": f"Database error: {str(e)}",
                "data": False
            }), 500
        
    @api_blueprint.route('/update_platform_account', methods=['POST'])
    def update_platform_account():
        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "message": "No data provided.",
                "data": False
            }), 400

        account_id = data.get('id')
        if not account_id:
            return jsonify({
                "status": "error",
                "message": "Field 'id' is required.",
                "data": False
            }), 400

        # Fetch the PlatformAuth instance
        platform_auth = g.session.query(PlatformAuth).filter_by(id=account_id).first()
        if not platform_auth:
            return jsonify({
                "status": "error",
                "message": f"Platform account with id {account_id} does not exist.",
                "data": False
            }), 404

        # Update fields if they are provided
        platform_id = data.get('platform_id')
        username = data.get('username')
        password = data.get('password')
        account_domain = data.get('account_domain')
        token = data.get('token')

        if platform_id:
            # Check if the platform exists
            platform = g.session.query(Platform).filter_by(id=platform_id).first()
            if not platform:
                return jsonify({
                    "status": "error",
                    "message": f"Platform with id {platform_id} does not exist.",
                    "data": False
                }), 404
            platform_auth.platform_id = platform_id

        if username is not None:
            platform_auth.username = username
        if password is not None:
            platform_auth.password = password
        if account_domain is not None:
            platform_auth.account_domain = account_domain
        if token is not None:
            platform_auth.token = token

        try:
            g.session.commit()
            auth_data = platform_auth.to_dict()
            return jsonify({
                "status": "success",
                "message": "Platform account updated successfully.",
                "data": auth_data
            }), 200
        except Exception as e:
            g.session.rollback()
            return jsonify({
                "status": "error",
                "message": f"Database error: {str(e)}",
                "data": False
            }), 500
    
    @api_blueprint.route('/delete_platform_account/<int:id>', methods=['DELETE'])
    @requires_consent
    def delete_platform_account(id):
        try:        
            platform_auth = g.session.query(PlatformAuth).filter_by(id=id).first()

            if platform_auth is None:
                return jsonify({
                            "status": "error",
                            "message": "No account found.",
                            "data": False
                        }), 404

            g.session.delete(platform_auth)
            g.session.commit()
            return jsonify({
                "status": "succcess",
                "message": "Account was deleted successfully"
            }), 200

        except Exception as e:
            g.session.rollback()  # Rollback in case of any error
            return jsonify({"error": str(e)}), 500


    @api_blueprint.route('/platform_accounts/<int:id>', methods=['GET'])
    @requires_consent
    def get_account(id):
        auth = g.session.query(PlatformAuth).get(id)
        if auth is None:
            return jsonify({
                            "status": "error",
                            "message": "No accounts found.",
                            "data": False
                        }), 404
        return jsonify({
                            "status": "success",
                            "message": "Account data returned.",
                            "data": auth.to_dict()
                        }), 404

    @api_blueprint.route('/get_all_platforms', methods=['GET'])
    @requires_consent
    def get_all_platforms():
        # Fetch configurations from the database
        allow_remote_config = g.session.query(Configuration).filter_by(key='allow_api_communication').first()
        api_token_config = g.session.query(Configuration).filter_by(key='api_token').first()

        # Check if remote API communication is allowed
        allow_remote = allow_remote_config.value == '1' if allow_remote_config else False

        # Check if API token is available
        api_token = api_token_config.value if api_token_config else None

        if allow_remote and api_token:
            # Proceed to send request to remote API
            try:
                session_requests = requests.Session()
                session_requests.headers.update({
                    'Origin': 'www.katomart.com',
                    'Authorization': f'Bearer {api_token}'
                })

                # Define the remote API URL
                remote_url = 'https://api.katomart.com/user-services/katomart_platforms'

                # Send GET request to the remote API
                response = session_requests.get(remote_url)

                if response.status_code == 200:
                    remote_platforms = response.json().get('data', [])

                    for remote_platform in remote_platforms:
                        platform_id = remote_platform['id']
                        platform = g.session.query(Platform).filter_by(id=platform_id).first()

                        # Map remote data to Platform fields
                        platform_data = {
                            'name': remote_platform.get('name'),
                            'base_url': remote_platform.get('baseUrl'),
                            'active': remote_platform.get('active', True),
                            'account_requires_specific_url': remote_platform.get('account_requires_specific_url', False),
                            'url_description': remote_platform.get('url_description'),
                            'may_have_issues': remote_platform.get('may_have_issues', False),
                            'has_issues': remote_platform.get('has_issues', False),
                            'issues_description': remote_platform.get('issues_description'),
                            'created_at': remote_platform.get('createdAt'),
                            'updated_at': remote_platform.get('updatedAt'),
                        }

                        # Handle Platform
                        if platform:
                            # Update existing platform
                            for key, value in platform_data.items():
                                if value is not None:
                                    setattr(platform, key, value)
                        else:
                            # Insert new platform
                            platform = Platform(id=platform_id, **platform_data)
                            g.session.add(platform)

                        # Handle PlatformURLs
                        for remote_url in remote_platform.get('urls', []):
                            url_id = remote_url['id']
                            url = g.session.query(PlatformURL).filter_by(id=url_id).first()

                            # Map remote data to PlatformURL fields with type conversion
                            url_data = {
                                'platform_id': remote_url.get('platformId') or platform_id,
                                'url_kind': remote_url.get('urlKind'),
                                'url': remote_url.get('url'),
                                'has_f_string': remote_url.get('hasFString', False),
                                'f_string_params': remote_url.get('fStringParams'),
                                'is_active': remote_url.get('isActive', True),
                                'needs_specific_headers': remote_url.get('needsSpecificHeaders', False),
                                'specific_headers': remote_url.get('specificHeaders'),
                                'accepts_raw_request': remote_url.get('acceptsRawRequest', False),
                                'has_visitation_limit': remote_url.get('hasVisitationLimit', False),
                                'visitation_limit': remote_url.get('visitationLimit'),
                                'visitation_count': remote_url.get('visitationCount', 0),
                                'created_at': remote_url.get('createdAt'),
                                'updated_at': remote_url.get('updatedAt'),
                            }

                            if url:
                                # Update existing URL
                                for key, value in url_data.items():
                                    if value is not None:
                                        setattr(url, key, value)
                            else:
                                # Insert new URL
                                url = PlatformURL(id=url_id, **url_data)
                                g.session.add(url)
                    g.session.commit()
                else:
                    # If the request failed, log the error and proceed without updating the database
                    print(f"Failed to fetch platforms from remote API. Status code: {response.status_code}")
            except Exception as e:
                # Log the exception and proceed without updating the database
                print(f"Error fetching platforms from remote API: {e}")

        # Query the local database for platforms
        all_platforms = g.session.query(Platform).all()
        if not all_platforms:
            return jsonify({
                "status": "error",
                "message": "No platforms found.",
                "data": False
            }), 404

        return jsonify({
            "status": "success",
            "message": "Fetched all platforms.",
            "data": [platform.to_dict() for platform in all_platforms]
        }), 200
    
    @api_blueprint.route('/platforms/<int:id>', methods=['GET'])
    @requires_consent
    def get_platform(id):
        platform = g.session.query(Platform).get(id)
        if platform is None:
            return jsonify({
                            "status": "error",
                            "message": "Platform was not found.",
                            "data": False
                        }), 404
        return jsonify({
                            "status": "success",
                            "message": "Fetched platform.",
                            "data": platform.to_dict()
                        }), 200

    @api_blueprint.route('/get_all_courses')
    @requires_consent
    def get_all_courses():
        all_courses = g.session.query(Course).all()
        if all_courses is None:
            return jsonify({
                            "status": "error",
                            "message": "No courses found.",
                            "data": False
                        }), 404
        return jsonify({
                            "status": "success",
                            "message": "Fetched all courses.",
                            "data": [course.to_dict() for course in all_courses]
                        }), 200
    
    @api_blueprint.route('/courses/bulk', methods=['POST'])
    @requires_consent
    def get_courses_bulk():
        katomart_ids = request.json.get('katomart_ids', [])
        courses = g.session.query(Course).filter(Course.katomart_id.in_(katomart_ids)).all()
        if not courses:
            return jsonify({
                "status": "error",
                "message": "Courses not found.",
                "data": False
            }), 404
        return jsonify({
            "status": "success",
            "message": "Fetched courses information.",
            "data": [course.to_dict() for course in courses]
        }), 200

    @api_blueprint.route('/courses/<int:katomart_id>', methods=['GET'])
    @requires_consent
    def get_course(katomart_id):
        course = g.session.query(Course).get(katomart_id)
        if course is None:
            return jsonify({
                "status": "error",
                "message": "Course not found.",
                "data": False
            }), 404
        return jsonify({
        "status": "success",
        "message": "Fetched course information.",
        "data": course.to_dict()
    }), 200

    @api_blueprint.route('/modules/<int:id>', methods=['GET'])
    @requires_consent
    def get_module(id):
        module = g.session.query(Module).get(id).first()
        if module is None:
            return jsonify({
                            "status": "error",
                            "message": "Module not found.",
                            "data": False
                        }), 404
        return jsonify({
                            "status": "success",
                            "message": "Fetched module information.",
                            "data": module.to_dict()
                        }), 200

    @api_blueprint.route('/lessons/<int:id>', methods=['GET'])
    @requires_consent
    def get_lesson(id):
        lesson = g.session.query(Lesson).get(id)
        if lesson is None:
            return jsonify({
                            "status": "error",
                            "message": "Lesson not found.",
                            "data": False
                        }), 404
        return jsonify({
                            "status": "success",
                            "message": "Fetched lesson information.",
                            "data": lesson.to_dict()
                        }), 200

    @api_blueprint.route('/files/<int:id>', methods=['GET'])
    @requires_consent
    def get_file(id):
        file = g.session.query(File).get(id)
        if file is None:
            return jsonify({
                            "status": "error",
                            "message": "File not found.",
                            "data": False
                        }), 404
        return jsonify({
                            "status": "success",
                            "message": "Fetched file information.",
                            "data": file.to_dict()
                        }), 200

    @api_blueprint.route('/courses/<int:katomart_id>', methods=['POST'])
    @requires_consent
    def update_course(katomart_id):
        course = g.session.query(Course).get(katomart_id)
        if course is None:
            return jsonify({
                "status": "error",
                "message": "Course not found.",
                "data": False
            }), 404

        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "message": "Invalid JSON payload.",
                "data": False
            }), 400

        # List of fields that can be updated
        updatable_fields = [
            'name', 'formatted_name', 'teacher', 'price', 'description', 'is_listed',
            'content_list_date', 'content_list_type', 'is_downloaded', 'download_date',
            'download_type', 'download_path', 'backed_up', 'backup_type', 'backup_date',
            'sent_cache_to_api', 'is_active', 'is_locked', 'unlocks_at', 'has_drm',
            'course_expires', 'access_expiration', 'platform_id', 'platform_auth_id', 'extra_data'
        ]

        for key, value in data.items():
            if key in updatable_fields:
                setattr(course, key, value)
            else:
                return jsonify({
                    "status": "error",
                    "message": f"Field '{key}' cannot be updated.",
                    "data": False
                }), 400

        try:
            g.session.commit()
        except Exception as e:
            g.session.rollback()
            return jsonify({
                "status": "error",
                "message": f"An error occurred while updating the course: {str(e)}",
                "data": False
            }), 500

        return jsonify({
            "status": "success",
            "message": "Course updated successfully.",
            "data": course.to_dict()
        }), 200

    @api_blueprint.route('/modules/<int:katomart_id>', methods=['POST'])
    @requires_consent
    def update_module(katomart_id):
        module = g.session.query(Module).get(katomart_id)
        if module is None:
            return jsonify({
                "status": "error",
                "message": "Module not found.",
                "data": False
            }), 404

        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "message": "Invalid JSON payload.",
                "data": False
            }), 400

        updatable_fields = [
            'name', 'formatted_name', 'order', 'description', 'is_active', 'is_locked',
            'unlocks_at', 'has_drm', 'is_listed', 'content_list_date', 'content_list_type',
            'should_download', 'is_downloaded', 'download_date', 'download_type', 'course_id', 'extra_data'
        ]

        for key, value in data.items():
            if key in updatable_fields:
                setattr(module, key, value)
            else:
                return jsonify({
                    "status": "error",
                    "message": f"Field '{key}' cannot be updated.",
                    "data": False
                }), 400

        try:
            g.session.commit()
        except Exception as e:
            g.session.rollback()
            return jsonify({
                "status": "error",
                "message": f"An error occurred while updating the module: {str(e)}",
                "data": False
            }), 500

        return jsonify({
            "status": "success",
            "message": "Module updated successfully.",
            "data": module.to_dict()
        }), 200

    @api_blueprint.route('/lessons/<int:katomart_id>', methods=['POST'])
    @requires_consent
    def update_lesson(katomart_id):
        lesson = g.session.query(Lesson).get(katomart_id)
        if lesson is None:
            return jsonify({
                "status": "error",
                "message": "Lesson not found.",
                "data": False
            }), 404

        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "message": "Invalid JSON payload.",
                "data": False
            }), 400

        updatable_fields = [
            'name', 'formatted_name', 'order', 'description', 'is_active', 'is_locked',
            'unlocks_at', 'has_drm', 'is_listed', 'content_list_date', 'content_list_type',
            'should_download', 'is_downloaded', 'download_date', 'download_type', 'module_id', 'extra_data'
        ]

        for key, value in data.items():
            if key in updatable_fields:
                setattr(lesson, key, value)
            else:
                return jsonify({
                    "status": "error",
                    "message": f"Field '{key}' cannot be updated.",
                    "data": False
                }), 400

        try:
            g.session.commit()
        except Exception as e:
            g.session.rollback()
            return jsonify({
                "status": "error",
                "message": f"An error occurred while updating the lesson: {str(e)}",
                "data": False
            }), 500

        return jsonify({
            "status": "success",
            "message": "Lesson updated successfully.",
            "data": lesson.to_dict()
        }), 200

    @api_blueprint.route('/files/<int:katomart_id>', methods=['POST'])
    @requires_consent
    def update_file(katomart_id):
        file = g.session.query(File).get(katomart_id)
        if file is None:
            return jsonify({
                "status": "error",
                "message": "File not found.",
                "data": False
            }), 404

        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "message": "Invalid JSON payload.",
                "data": False
            }), 400

        updatable_fields = [
            'name', 'formatted_name', 'order', 'description', 'is_active', 'is_locked',
            'should_download', 'unlocks_at', 'has_drm', 'is_decrypted', 'is_downloaded',
            'download_date', 'file_size', 'file_type', 'duration', 'lesson_id', 'extra_data'
        ]

        for key, value in data.items():
            if key in updatable_fields:
                setattr(file, key, value)
            else:
                return jsonify({
                    "status": "error",
                    "message": f"Field '{key}' cannot be updated.",
                    "data": False
                }), 400

        try:
            g.session.commit()
        except Exception as e:
            g.session.rollback()
            return jsonify({
                "status": "error",
                "message": f"An error occurred while updating the file: {str(e)}",
                "data": False
            }), 500

        return jsonify({
            "status": "success",
            "message": "File updated successfully.",
            "data": file.to_dict()
        }), 200

    def run_scraper(platform_name, auth_id, job_type, job_id, course_id=None):
        session = get_session()
        try:
            auth_data = session.query(PlatformAuth).filter_by(id=auth_id).first()
            if not auth_data:
                print(f"Authentication data not found for auth ID {auth_id}")
                return

            # Initialize the scraper
            platform_scraper = get_platform_scraper(platform_name, auth_data=auth_data, session=session, course_id=course_id)

            with scraper_manager_lock:
                # Store the scraper instance
                scraper_manager[job_id]['scraper'] = platform_scraper
                scraper_manager[job_id]['status'] = 'running'

            if job_type == 're_authenticate':
                course_data = platform_scraper.login()
            if job_type == 'list_courses':
                course_data = platform_scraper.get_course_data()
            if job_type == 'get_course_information':
                course_data = platform_scraper.get_product_information(course_id)
            if job_type == 'start_downloads':
                course_data = platform_scraper.start_downloads()

            platform_scraper.close()

            with scraper_manager_lock:
                # Update status after completion
                scraper_manager[job_id]['status'] = 'completed'

            print(f"Scraping and downloading completed for platform {platform_name} and auth ID {auth_id}")

        except Exception as e:
            print(f"An error occurred: {e}")
            session.rollback()
            with scraper_manager_lock:
                scraper_manager[job_id]['status'] = 'error'
        finally:
            session.close()
            # Clean up scraper_manager entry after completion
            with scraper_manager_lock:
                scraper_manager.pop(job_id, None)

    @api_blueprint.route('/start_scraper', methods=['POST'])
    def start_scraper():
        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "message": "No data provided.",
                "data": False
            }), 400

        platform_id = data.get('platform_id')
        course_id = data.get('course_id')        
        platform_auth = g.session.query(PlatformAuth).filter_by(platform_id=platform_id).first()
        auth_id = platform_auth.id
        job_type = data.get('job_type')

        if not platform_id or not auth_id or not job_type:
            return jsonify({
                "status": "error",
                "message": "Both 'platform_id', 'auth_id' and 'job_type' are required.",
                "data": False
            }), 400

        # Fetch the Platform information
        platform = g.session.query(Platform).filter_by(id=platform_id).first()
        if not platform:
            return jsonify({
                "status": "error",
                "message": "Platform not found.",
                "data": False
            }), 404

        platform_name = platform.name.lower()

        job_id = str(uuid4())

        with scraper_manager_lock:
            scraper_manager[job_id] = {'status': 'starting', 'scraper': None}

        try:
            scraper_thread = threading.Thread(target=run_scraper, args=(platform_name, auth_id, job_type, job_id, course_id))
            with scraper_manager_lock:
                scraper_manager[job_id]['thread'] = scraper_thread
                scraper_manager[job_id]['status'] = 'running'
                print(f"Scraper for job_id {job_id} has been stored in scraper_manager")
            scraper_thread.start()
            print(f"Scraper thread for job_id {job_id} started successfully")
        except Exception as e:
            print(f"Error starting scraper thread for job_id {job_id}: {str(e)}")

        return jsonify({
            "status": "success",
            "message": "Scraper has been initiated.",
            "data": {"job_id": job_id}
        }), 200

    @api_blueprint.route('/pause_scraper', methods=['POST'])
    def pause_scraper():
        data = request.get_json()
        job_id = data.get('job_id')
        with scraper_manager_lock:
            scraper_info = scraper_manager.get(job_id)
        if scraper_info and scraper_info['scraper']:
            scraper_info['scraper'].pause()
            with scraper_manager_lock:
                scraper_info['status'] = 'paused'
            return jsonify({"status": "success", "message": "Scraper paused."}), 200
        else:
            return jsonify({"status": "error", "message": "Scraper not found."}), 404

    @api_blueprint.route('/resume_scraper', methods=['POST'])
    def resume_scraper():
        data = request.get_json()
        job_id = data.get('job_id')
        with scraper_manager_lock:
            scraper_info = scraper_manager.get(job_id)
        if scraper_info and scraper_info['scraper']:
            scraper_info['scraper'].resume()
            with scraper_manager_lock:
                scraper_info['status'] = 'running'
            return jsonify({"status": "success", "message": "Scraper resumed."}), 200
        else:
            return jsonify({"status": "error", "message": "Scraper not found."}), 404

    @api_blueprint.route('/stop_scraper', methods=['POST'])
    def stop_scraper():
        data = request.get_json()
        job_id = data.get('job_id')
        with scraper_manager_lock:
            scraper_info = scraper_manager.get(job_id)
        if scraper_info and scraper_info['scraper']:
            scraper_info['scraper'].stop()
            with scraper_manager_lock:
                scraper_info['status'] = 'stopped'
            return jsonify({"status": "success", "message": "Scraper stopped."}), 200
        else:
            return jsonify({"status": "error", "message": "Scraper not found."}), 404

    @api_blueprint.route('/scraper_status', methods=['GET'])
    def scraper_status():
        job_id = request.args.get('job_id')
        with scraper_manager_lock:
            scraper_info = scraper_manager.get(job_id)
        if scraper_info:
            status = scraper_info['status']
            progress = scraper_info['scraper'].progress if scraper_info['scraper'] else 0
            return jsonify({
                "status": "success",
                "data": {
                    "job_id": job_id,
                    "scraper_status": status,
                    "progress": progress
                }
            }), 200
        else:
            return jsonify({"status": "error", "message": "Scraper not found."}), 404

    @api_blueprint.route('/get_course_details/<int:katomart_id>', methods=['GET'])
    def get_course_details(katomart_id):
        try:
            course = g.session.query(Course).filter_by(katomart_id=katomart_id).first()
            if not course:
                return jsonify({
                    "status": "error",
                    "message": "Course not found",
                    "data": None
                }), 404

            course_data = course.to_dict(
                    include_platform=True,
                    include_modules=True
                )

            return jsonify({
                "status": "success",
                "message": "Course details fetched successfully",
                "data": course_data
            }), 200
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e),
                "data": None
            }), 500
    

    # --------- Video Notes Routes ---------

    @api_blueprint.route('/video_notes', methods=['POST'])
    def save_video_note():
        """
        Save a new video note.
        Expected JSON payload:
        {
            "fileId": <int>,
            "time": <float>,
            "text": <string>
        }
        """
        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "message": "No data provided.",
                "data": False
            }), 400

        file_id = data.get('fileId')
        time = data.get('time')
        text = data.get('text')

        if file_id is None or time is None or text is None:
            return jsonify({
                "status": "error",
                "message": "Fields 'fileId', 'time', and 'text' are required.",
                "data": False
            }), 400

        # Check if the file exists
        file = g.session.query(File).filter_by(katomart_id=file_id).first()
        if not file:
            return jsonify({
                "status": "error",
                "message": f"File with katomart_id {file_id} does not exist.",
                "data": False
            }), 404

        # Create a new VideoNote instance
        new_note = VideoNote(
            file_id=file_id,
            time=time,
            text=text
        )

        try:
            g.session.add(new_note)
            g.session.commit()

            return jsonify({
                "status": "success",
                "message": "Video note saved successfully.",
                "data": new_note.to_dict()
            }), 201
        except Exception as e:
            g.session.rollback()
            return jsonify({
                "status": "error",
                "message": f"Database error: {str(e)}",
                "data": False
            }), 500


    @api_blueprint.route('/video_notes', methods=['GET'])
    def get_video_notes():
        """
        Retrieve video notes for a specific file.
        Query Parameters:
            - fileId: katomart_id of the file
        """
        file_id = request.args.get('fileId')

        if not file_id:
            return jsonify({
                "status": "error",
                "message": "Query parameter 'fileId' is required.",
                "data": False
            }), 400

        try:
            file_id = int(file_id)
        except ValueError:
            return jsonify({
                "status": "error",
                "message": "Query parameter 'fileId' must be an integer.",
                "data": False
            }), 400

        # Check if the file exists
        file = g.session.query(File).filter_by(katomart_id=file_id).first()
        if not file:
            return jsonify({
                "status": "error",
                "message": f"File with katomart_id {file_id} does not exist.",
                "data": False
            }), 404

        # Retrieve all video notes for the file
        notes = g.session.query(VideoNote).filter_by(file_id=file_id).all()

        return jsonify({
            "status": "success",
            "message": f"Fetched {len(notes)} video note(s).",
            "data": [note.to_dict() for note in notes]
        }), 200


    @api_blueprint.route('/video_notes/<int:note_id>', methods=['PUT'])
    def update_video_note(note_id):
        """
        Update an existing video note.
        URL Parameter:
            - note_id: ID of the video note to update
        Expected JSON payload (any of the following fields):
        {
            "time": <float>,      # Optional
            "text": <string>      # Optional
        }
        """
        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "message": "No data provided.",
                "data": False
            }), 400

        # Fetch the VideoNote instance
        note = g.session.query(VideoNote).filter_by(id=note_id).first()
        if not note:
            return jsonify({
                "status": "error",
                "message": f"Video note with id {note_id} does not exist.",
                "data": False
            }), 404

        # Update fields if provided
        time = data.get('time')
        text = data.get('text')

        if time is not None:
            note.time = time
        if text is not None:
            note.text = text

        try:
            g.session.commit()
            return jsonify({
                "status": "success",
                "message": "Video note updated successfully.",
                "data": note.to_dict()
            }), 200
        except Exception as e:
            g.session.rollback()
            return jsonify({
                "status": "error",
                "message": f"Database error: {str(e)}",
                "data": False
            }), 500


    # --------- PDF Annotations Routes ---------

    @api_blueprint.route('/pdf_annotations', methods=['POST'])
    def save_pdf_annotations():
        """
        Save PDF annotations for a specific file.
        Expected JSON payload:
        {
            "fileId": <int>,
            "annotations": <dict>  # JSON data representing annotations
        }
        """
        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "message": "No data provided.",
                "data": False
            }), 400

        file_id = data.get('fileId')
        annotations = data.get('annotations')

        if file_id is None or annotations is None:
            return jsonify({
                "status": "error",
                "message": "Fields 'fileId' and 'annotations' are required.",
                "data": False
            }), 400

        # Check if the file exists
        file = g.session.query(File).filter_by(katomart_id=file_id).first()
        if not file:
            return jsonify({
                "status": "error",
                "message": f"File with katomart_id {file_id} does not exist.",
                "data": False
            }), 404

        # Check if a PdfAnnotation already exists for this file
        existing_annotation = g.session.query(PdfAnnotation).filter_by(file_id=file_id).first()

        if existing_annotation:
            # Update existing annotations
            existing_annotation.annotations = annotations
            message = "PDF annotations updated successfully."
        else:
            # Create a new PdfAnnotation instance
            new_annotation = PdfAnnotation(
                file_id=file_id,
                annotations=annotations
            )
            g.session.add(new_annotation)
            message = "PDF annotations saved successfully."

        try:
            g.session.commit()
            annotation = existing_annotation if existing_annotation else new_annotation
            return jsonify({
                "status": "success",
                "message": message,
                "data": annotation.to_dict()
            }), 200
        except Exception as e:
            g.session.rollback()
            return jsonify({
                "status": "error",
                "message": f"Database error: {str(e)}",
                "data": False
            }), 500


    @api_blueprint.route('/pdf_annotations', methods=['GET'])
    def get_pdf_annotations():
        """
        Retrieve PDF annotations for a specific file.
        Query Parameters:
            - fileId: katomart_id of the file
        """
        file_id = request.args.get('fileId')

        if not file_id:
            return jsonify({
                "status": "error",
                "message": "Query parameter 'fileId' is required.",
                "data": False
            }), 400

        try:
            file_id = int(file_id)
        except ValueError:
            return jsonify({
                "status": "error",
                "message": "Query parameter 'fileId' must be an integer.",
                "data": False
            }), 400

        # Check if the file exists
        file = g.session.query(File).filter_by(katomart_id=file_id).first()
        if not file:
            return jsonify({
                "status": "error",
                "message": f"File with katomart_id {file_id} does not exist.",
                "data": False
            }), 404

        # Retrieve PDF annotations for the file
        annotation = g.session.query(PdfAnnotation).filter_by(file_id=file_id).first()

        if annotation:
            return jsonify({
                "status": "success",
                "message": "Fetched PDF annotations.",
                "data": annotation.to_dict()
            }), 200
        else:
            return jsonify({
                "status": "success",
                "message": "No PDF annotations found for this file.",
                "data": {}
            }), 200


    @api_blueprint.route('/pdf_annotations/<int:annotation_id>', methods=['PUT'])
    def update_pdf_annotations(annotation_id):
        """
        Update an existing PDF annotation.
        URL Parameter:
            - annotation_id: ID of the PDF annotation to update
        Expected JSON payload:
        {
            "annotations": <dict>  # Updated annotations data
        }
        """
        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "message": "No data provided.",
                "data": False
            }), 400

        annotations = data.get('annotations')

        if annotations is None:
            return jsonify({
                "status": "error",
                "message": "Field 'annotations' is required.",
                "data": False
            }), 400

        # Fetch the PdfAnnotation instance
        annotation = g.session.query(PdfAnnotation).filter_by(id=annotation_id).first()
        if not annotation:
            return jsonify({
                "status": "error",
                "message": f"PDF annotation with id {annotation_id} does not exist.",
                "data": False
            }), 404

        # Update annotations
        annotation.annotations = annotations

        try:
            g.session.commit()
            return jsonify({
                "status": "success",
                "message": "PDF annotations updated successfully.",
                "data": annotation.to_dict()
            }), 200
        except Exception as e:
            g.session.rollback()
            return jsonify({
                "status": "error",
                "message": f"Database error: {str(e)}",
                "data": False
            }), 500

    @api_blueprint.route('/update_attribute', methods=['POST'])
    @requires_consent
    def update_attribute():
        data = request.json
        if not data:
            return jsonify({
                "status": "error",
                "message": "No data provided.",
                "data": False
            }), 400

        action = data.get('action')
        katomart_id = data.get('katomart_id')
        value = data.get('value')

        if not action or katomart_id is None or value is None:
            return jsonify({
                "status": "error",
                "message": "Action, katomart_id, and value are required.",
                "data": False
            }), 400

        # Map action to model and attribute
        action_mapping = {
            'update_course_formatted_name': (Course, 'formatted_name'),
            'update_module_formatted_name': (Module, 'formatted_name'),
            'update_module_should_download': (Module, 'should_download'),
            'update_lesson_formatted_name': (Lesson, 'formatted_name'),
            'update_lesson_should_download': (Lesson, 'should_download'),
            'update_file_formatted_name': (File, 'formatted_name'),
            'update_file_should_download': (File, 'should_download'),
        }

        if action not in action_mapping:
            return jsonify({
                "status": "error",
                "message": "Invalid action.",
                "data": False
            }), 400

        model_class, attribute_name = action_mapping[action]

        # Fetch the object by katomart_id
        obj = g.session.query(model_class).filter_by(katomart_id=katomart_id).first()
        if not obj:
            return jsonify({
                "status": "error",
                "message": f"{model_class.__name__} with katomart_id {katomart_id} not found.",
                "data": False
            }), 404

        # Update the attribute
        setattr(obj, attribute_name, value)
        obj.updated_at = int(datetime.datetime.now().timestamp())

        g.session.commit()

        return jsonify({
            "status": "success",
            "message": f"{model_class.__name__} updated successfully.",
            "data": obj.to_dict()
        }), 200

    @api_blueprint.route('/manage-running-scraper', methods=['POST'])
    @requires_consent
    def manage_running_scraper():
        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "message": "No data provided.",
                "data": False
            }), 400

        action = data.get('action')
        job_id = data.get('job_id')
        payload_data = data.get('data')

        if not action or not job_id:
            return jsonify({
                "status": "error",
                "message": "'action' and 'job_id' are required.",
                "data": False
            }), 400

        with scraper_manager_lock:
            scraper_info = scraper_manager.get(job_id)

        if not scraper_info:
            return jsonify({
                "status": "error",
                "message": f"No scraper running with job_id {job_id}.",
                "data": False
            }), 404

        scraper = scraper_info.get('scraper')

        if not scraper:
            return jsonify({
                "status": "error",
                "message": "Scraper instance not found.",
                "data": False
            }), 500

        allowed_actions = [
            'pause', 'resume', 'stop',
            'add_to_normal_queue', 'add_to_priority_queue',
            'remove_from_normal_queue', 'remove_from_priority_queue',
            'demote_from_priority_queue'
        ]

        if action not in allowed_actions:
            return jsonify({
                "status": "error",
                "message": f"Invalid action '{action}'.",
                "data": False
            }), 400

        try:
            if action == 'pause':
                scraper.pause()
                message = "Scraper paused."
            elif action == 'resume':
                scraper.resume()
                message = "Scraper resumed."
            elif action == 'stop':
                scraper.stop()
                message = "Scraper stopped."
            elif action in [
                'add_to_normal_queue', 'add_to_priority_queue',
                'remove_from_normal_queue', 'remove_from_priority_queue',
                'demote_from_priority_queue'
            ]:
                if not payload_data or 'katomart_id' not in payload_data:
                    return jsonify({
                        "status": "error",
                        "message": f"'data' with 'katomart_id' is required for action '{action}'.",
                        "data": False
                    }), 400

                katomart_id = payload_data['katomart_id']

                # Fetch the File object from the database
                file = g.session.query(Lesson).filter_by(katomart_id=katomart_id).first()
                if not file:
                    return jsonify({
                        "status": "error",
                        "message": f"Lesson with katomart_id {katomart_id} not found.",
                        "data": False
                    }), 404

                # Create file_info dictionary
                file_info = file.to_dict()

                if action == 'add_to_normal_queue':
                    scraper.add_to_normal_queue(file_info)
                    message = "File added to normal queue."
                elif action == 'add_to_priority_queue':
                    scraper.add_to_priority_queue(file_info)
                    message = "File added to priority queue."
                elif action == 'remove_from_normal_queue':
                    scraper.remove_from_normal_queue(file_info)
                    message = "File removed from normal queue."
                elif action == 'remove_from_priority_queue':
                    scraper.remove_from_priority_queue(file_info)
                    message = "File removed from priority queue."
                elif action == 'demote_from_priority_queue':
                    scraper.demote_from_priority_queue(file_info)
                    message = "File demoted from priority queue to normal queue."
            else:
                return jsonify({
                    "status": "error",
                    "message": "Unhandled action.",
                    "data": False
                }), 500

            return jsonify({
                "status": "success",
                "message": message,
                "data": True
            }), 200

        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e),
                "data": False
            }), 500

    @api_blueprint.route('/submit_platform_report', methods=['POST'])
    @requires_consent
    def submit_platform_report():
        # Fetch configurations from the database
        allow_remote_config = g.session.query(Configuration).filter_by(key='allow_api_communication').first()
        api_token_config = g.session.query(Configuration).filter_by(key='api_token').first()

        # Check if remote API communication is allowed
        allow_remote = allow_remote_config.value == '1' if allow_remote_config else False

        # Check if API token is available
        api_token = api_token_config.value if api_token_config else None

        # Get the report data from the request
        report_data = request.get_json()

        if not report_data:
            return jsonify({
                "status": "error",
                "message": "No data provided.",
                "data": False
            }), 400

        # Extract data from report_data
        platform_id = report_data.get('platform')
        course_id = report_data.get('course')
        description = report_data.get('description')
        send_debug_data = report_data.get('sendDebugData', False)
        access_token = report_data.get('accessToken')

        if not platform_id or not course_id or not description:
            return jsonify({
                "status": "error",
                "message": "Missing required fields: platform, course, or description.",
                "data": False
            }), 400



        # Prepare data to send to the remote API
        remote_report_data = {
            "platformId": platform_id,  # Assuming the remote API requires platform ID
            "course_id": course_id,
            "description": description,
            "usage_logs": [],  # Include usage logs if available
            "course_access_token": access_token,
        }

        if allow_remote and api_token:
            # Proceed to send request to remote API
            try:
                session_requests = requests.Session()
                session_requests.headers.update({
                    'Origin': 'www.katomart.com',
                    'Authorization': f'Bearer {api_token}',
                    'Content-Type': 'application/json'
                })

                # Define the remote API URL
                remote_url = 'https://api.katomart.com/user-services/create-platform-report'

                # Send POST request to the remote API
                response = session_requests.post(remote_url, json=remote_report_data)

                if response.status_code == 201:
                    remote_response = response.json()
                    return jsonify({
                        "status": "success",
                        "message": "Platform report submitted successfully.",
                        "data": remote_response
                    }), 201
                else:
                    # If the request failed, log the error and return response
                    print(f"Failed to submit platform report to remote API. Status code: {response.status_code}")
                    return jsonify({
                        "status": "error",
                        "message": "Failed to submit platform report to remote API.",
                        "data": response.text
                    }), response.status_code
            except Exception as e:
                # Log the exception and proceed without updating the database
                print(f"Error submitting platform report to remote API: {e}")
                return jsonify({
                    "status": "error",
                    "message": "Exception occurred while submitting to remote API.",
                    "data": str(e)
                }), 500
        else:
            # If remote communication is not allowed, return an error
            return jsonify({
                "status": "error",
                "message": "Remote API communication is disabled or API token is missing.",
                "data": False
            }), 403

    @api_blueprint.route('/get_course_progress/<int:katomart_id>', methods=['GET'])
    def get_course_progress(katomart_id):
        try:
            # Fetch the course along with its modules and lessons
            course = g.session.query(Course).options(
                joinedload(Course.modules)
                .joinedload(Module.lessons)
            ).filter(Course.katomart_id == katomart_id).first()

            if not course:
                return jsonify({
                    "status": "error",
                    "message": "Course not found",
                    "data": None
                }), 404

            # Collect lessons with required attributes
            lessons = []
            for module in course.modules:
                for lesson in module.lessons:
                    lesson_data = {
                        'katomart_id': lesson.katomart_id,
                        'is_downloaded': bool(lesson.is_downloaded),
                        'download_date': int(lesson.download_date) if lesson.download_date else None
                    }
                    lessons.append(lesson_data)

            return jsonify({
                "status": "success",
                "message": "Course progress fetched successfully",
                "data": lessons
            }), 200

        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e),
                "data": None
            }), 500
