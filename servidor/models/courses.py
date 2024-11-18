import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, BigInteger, JSON, Float
from sqlalchemy.orm import relationship

from . import Base
from .dblog import Log


class PlatformAuth(Base):
    __tablename__ = 'platform_auths'

    id = Column(Integer, primary_key=True)
    platform_id = Column(Integer, ForeignKey('platforms.id'))
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    token = Column(String)
    account_domain = Column(String)
    refresh_token = Column(String)
    total_products = Column(Integer)
    token_expires_at = Column(BigInteger)
    extra_data = Column(JSON)
    is_logged_in = Column(Boolean, default=False)
    valid_combination = Column(Boolean, default=False)
    created_at = Column(BigInteger, default=lambda: int(datetime.datetime.now().timestamp()))
    updated_at = Column(BigInteger, default=lambda: int(datetime.datetime.now().timestamp()), onupdate=lambda: int(datetime.datetime.now().timestamp()))
    
    logs = relationship("Log", back_populates="platform_auth")
    platform = relationship("Platform", back_populates="auths")
    courses = relationship("Course", back_populates="platform_auth")

    def to_dict(self, include_platform=True):
        result = {
            'id': self.id,
            'platform_id': int(self.platform_id),
            'username': self.username.decode('utf-8') if isinstance(self.username, bytes) else self.username,
            'password': self.password.decode('utf-8') if isinstance(self.password, bytes) else self.password,
            'token': self.token.decode('utf-8') if isinstance(self.token, bytes) else self.token,
            'account_domain': self.account_domain.decode('utf-8') if isinstance(self.account_domain, bytes) else self.account_domain,
            'refresh_token': self.refresh_token.decode('utf-8') if isinstance(self.refresh_token, bytes) else self.refresh_token,
            'total_products': self.total_products,
            'token_expires_at': int(self.token_expires_at) if self.token_expires_at else None,
            'extra_data': self.extra_data,
            'is_logged_in': bool(self.is_logged_in),
            'valid_combination': bool(self.valid_combination),
            'created_at': int(self.created_at),
            'updated_at': int(self.updated_at),
        }

        if include_platform and self.platform:
            result['platform'] = self.platform.to_dict(include_auths=False)  # Prevent recursion
        return result

class PlatformURL(Base):
    __tablename__ = 'platform_urls'
    id = Column(String, primary_key=True)
    platform_id = Column(Integer, ForeignKey('platforms.id'), nullable=False)
    url_kind = Column(String) # Login, dashboard, api, product
    has_f_string = Column(Boolean, default=False)
    f_string_params = Column(JSON)
    is_active = Column(Boolean, default=True)
    needs_specific_headers = Column(Boolean, default=False)
    specific_headers = Column(JSON)
    accepts_raw_request = Column(Boolean, default=False)
    has_visitation_limit = Column(Boolean, default=False)
    visitation_limit = Column(Integer)
    visitation_count = Column(Integer, default=0)
    url = Column(String)
    created_at = Column(BigInteger, default=lambda: int(datetime.datetime.now().timestamp()))
    updated_at = Column(BigInteger, default=lambda: int(datetime.datetime.now().timestamp()), onupdate=lambda: int(datetime.datetime.now().timestamp()))
    platform = relationship("Platform", back_populates="urls")
    def to_dict(self):
        return {
            'id': self.id.decode('utf-8') if isinstance(self.id, bytes) else self.id,
            'platform_id': int(self.platform_id),
            'url_kind': self.url_kind.decode('utf-8') if isinstance(self.url_kind, bytes) else self.url_kind,
            'has_f_string': bool(self.has_f_string),
            'f_string_params': self.f_string_params,
            'is_active': bool(self.is_active),
            'needs_specific_headers': bool(self.needs_specific_headers),
            'specific_headers': self.specific_headers,
            'accepts_raw_request': bool(self.accepts_raw_request),
            'has_visitation_limit': bool(self.has_visitation_limit),
            'visitation_limit': self.visitation_limit,
            'visitation_count': self.visitation_count,
            'url': self.url.decode('utf-8') if isinstance(self.url, bytes) else self.url,
            'created_at': int(self.created_at),
            'updated_at': int(self.updated_at),
            # Add nested relationship if needed
            'platform': self.platform.to_dict() if self.platform else None
        }

class Platform(Base):
    __tablename__ = 'platforms'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    base_url = Column(String)
    active = Column(Boolean, default=True)
    account_requires_specific_url = Column(Boolean, default=False)
    url_description = Column(String)
    may_have_issues = Column(Boolean, default=False)
    has_issues = Column(Boolean, default=False)
    issues_description = Column(String)
    created_at = Column(BigInteger, default=lambda: int(datetime.datetime.now().timestamp()))
    updated_at = Column(BigInteger, default=lambda: int(datetime.datetime.now().timestamp()), onupdate=lambda: int(datetime.datetime.now().timestamp()))
    auths = relationship("PlatformAuth", back_populates="platform")
    courses = relationship("Course", back_populates="platform")
    urls = relationship("PlatformURL", back_populates="platform", cascade="all, delete, delete-orphan")
    logs = relationship("Log", back_populates="platform")

    def to_dict(self, include_auths=True, include_courses=True):
        result = {
            'id': int(self.id),
            'name': self.name.decode('utf-8') if isinstance(self.name, bytes) else self.name,
            'base_url': self.base_url.decode('utf-8') if isinstance(self.base_url, bytes) else self.base_url,
            'active': bool(self.active),
            'account_requires_specific_url': bool(self.account_requires_specific_url),
            'url_description': self.url_description.decode('utf-8') if isinstance(self.url_description, bytes) else self.url_description,
            'may_have_issues': bool(self.may_have_issues),
            'has_issues': bool(self.has_issues),
            'issues_description': self.issues_description.decode('utf-8') if isinstance(self.issues_description, bytes) else self.issues_description,
            'created_at': int(self.created_at),
            'updated_at': int(self.updated_at),
            'urls': [url.to_dict() for url in self.urls] if self.urls else []
        }

        if include_auths:
            result['auths'] = [auth.to_dict(include_platform=False) for auth in self.auths]  # Prevent recursion
        if include_courses:
            result['courses'] = [course.to_dict(include_platform=False) for course in self.courses] if self.courses else []

        return result

class Course(Base):
    __tablename__ = 'courses'
    katomart_id = Column(Integer, primary_key=True)
    id = Column(String)
    extra_data = Column(JSON)
    name = Column(String)
    formatted_name = Column(String)
    teacher = Column(String)
    price = Column(Float)
    description = Column(String)
    is_listed = Column(Boolean, default=False)
    content_list_date = Column(BigInteger)
    content_list_type = Column(String)
    is_downloaded = Column(Boolean, default=False)
    download_date = Column(BigInteger)
    download_type = Column(String)
    download_path = Column(String)
    backed_up = Column(Boolean, default=False)
    backup_type = Column(String)
    backup_date = Column(BigInteger)
    sent_cache_to_api = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    is_locked = Column(Boolean, default=False)
    unlocks_at = Column(BigInteger)
    has_drm = Column(Boolean, default=False)
    course_expires = Column(Boolean, default=False)
    access_expiration = Column(BigInteger)
    created_at = Column(BigInteger, default=lambda: int(datetime.datetime.now().timestamp()))
    updated_at = Column(BigInteger, default=lambda: int(datetime.datetime.now().timestamp()), onupdate=lambda: int(datetime.datetime.now().timestamp()))
    platform_id = Column(Integer, ForeignKey('platforms.id'))
    platform_auth_id = Column(Integer, ForeignKey('platform_auths.id'))
    platform_auth = relationship("PlatformAuth", back_populates="courses")
    platform = relationship("Platform", back_populates="courses")
    modules = relationship("Module", back_populates="course")
    logs = relationship("Log", back_populates="course")

    def to_dict(self, include_platform=True, include_modules=True):
        result = {
            'katomart_id': self.katomart_id,
            'id': self.id.decode('utf-8') if isinstance(self.id, bytes) else self.id,
            'extra_data': self.extra_data,
            'name': self.name.decode('utf-8') if isinstance(self.name, bytes) else self.name,
            'formatted_name': self.formatted_name.decode('utf-8') if isinstance(self.formatted_name, bytes) else self.formatted_name,
            'teacher': self.teacher.decode('utf-8') if isinstance(self.teacher, bytes) else self.teacher,
            'price': self.price,
            'description': self.description.decode('utf-8') if isinstance(self.description, bytes) else (self.description or ''),
            'is_listed': bool(self.is_listed),
            'content_list_date': int(self.content_list_date) if self.content_list_date else None,
            'content_list_type': self.content_list_type.decode('utf-8') if isinstance(self.content_list_type, bytes) else self.content_list_type,
            'is_downloaded': bool(self.is_downloaded),
            'download_date': int(self.download_date) if self.download_date else None,
            'download_type': self.download_type.decode('utf-8') if isinstance(self.download_type, bytes) else self.download_type,
            'download_path': self.download_path.decode('utf-8') if isinstance(self.download_path, bytes) else self.download_path,
            'backed_up': bool(self.backed_up),
            'backup_type': self.backup_type.decode('utf-8') if isinstance(self.backup_type, bytes) else self.backup_type,
            'backup_date': int(self.backup_date) if self.backup_date else None,
            'sent_cache_to_api': bool(self.sent_cache_to_api),
            'is_active': bool(self.is_active),
            'is_locked': bool(self.is_locked),
            'unlocks_at': int(self.unlocks_at) if self.unlocks_at else None,
            'has_drm': bool(self.has_drm),
            'course_expires': bool(self.course_expires),
            'access_expiration': int(self.access_expiration) if self.access_expiration else None,
            'created_at': int(self.created_at),
            'updated_at': int(self.updated_at),
            'platform_id': self.platform_id,
            'platform_auth_id': self.platform_auth_id,
            'modules': [module.to_dict(include_course=False) for module in self.modules] if (include_modules and self.modules) else [],
            'logs': [log.to_dict() for log in self.logs] if self.logs else []
        }

        if include_platform and self.platform:
            result['platform'] = self.platform.to_dict(include_auths=False)  # Prevent recursion
        
        return result

class Module(Base):
    __tablename__ = 'modules'
    katomart_id = Column(Integer, primary_key=True)
    id = Column(String)
    extra_data = Column(JSON)
    name = Column(String)
    formatted_name = Column(String)
    order = Column(Integer)
    description = Column(String)
    is_active = Column(Boolean, default=False)
    is_locked = Column(Boolean, default=False)
    unlocks_at = Column(BigInteger)
    has_drm = Column(Boolean, default=False)
    is_listed = Column(Boolean, default=False)
    content_list_date = Column(BigInteger)
    content_list_type = Column(String)
    should_download = Column(Boolean, default=True)
    is_downloaded = Column(Boolean, default=False)
    download_date = Column(BigInteger)
    download_type = Column(String)
    created_at = Column(BigInteger, default=lambda: int(datetime.datetime.now().timestamp()))
    updated_at = Column(BigInteger, default=lambda: int(datetime.datetime.now().timestamp()), onupdate=lambda: int(datetime.datetime.now().timestamp()))
    course_id = Column(String, ForeignKey('courses.id'))
    course = relationship("Course", back_populates="modules")
    lessons = relationship("Lesson", back_populates="module")
    logs = relationship("Log", back_populates="module")

    def to_dict(self, include_course=True, include_lessons=True):
        result = {
            'katomart_id': self.katomart_id,
            'id': self.id.decode('utf-8') if isinstance(self.id, bytes) else self.id,
            'extra_data': self.extra_data,
            'name': self.name.decode('utf-8') if isinstance(self.name, bytes) else self.name,
            'formatted_name': self.formatted_name.decode('utf-8') if isinstance(self.formatted_name, bytes) else self.formatted_name,
            'order': int(self.order),
            'description': self.description.decode('utf-8') if isinstance(self.description, bytes) else (self.description or ''),
            'is_active': bool(self.is_active),
            'is_locked': bool(self.is_locked),
            'unlocks_at': int(self.unlocks_at) if self.unlocks_at else None,
            'has_drm': bool(self.has_drm),
            'is_listed': bool(self.is_listed),
            'content_list_date': int(self.content_list_date) if self.content_list_date else None,
            'content_list_type': self.content_list_type.decode('utf-8') if isinstance(self.content_list_type, bytes) else self.content_list_type,
            'should_download': bool(self.should_download),
            'is_downloaded': bool(self.is_downloaded),
            'download_date': int(self.download_date) if self.download_date else None,
            'download_type': self.download_type.decode('utf-8') if isinstance(self.download_type, bytes) else self.download_type,
            'created_at': int(self.created_at),
            'updated_at': int(self.updated_at),
            'lessons': [lesson.to_dict(include_module=False) for lesson in self.lessons] if (include_lessons and self.lessons) else []
        }

        if include_course:
            result['course'] = self.course.to_dict(include_platform=False) if self.course else None  # Prevent recursion
        return result

class Lesson(Base):
    __tablename__ = 'lessons'
    katomart_id = Column(Integer, primary_key=True)
    id = Column(String)
    extra_data = Column(JSON)
    name = Column(String)
    formatted_name = Column(String)
    order = Column(Integer)
    description = Column(String)
    is_active = Column(Boolean, default=False)
    is_locked = Column(Boolean, default=False)
    unlocks_at = Column(BigInteger)
    has_drm = Column(Boolean, default=False)
    is_listed = Column(Boolean, default=False)
    content_list_date = Column(BigInteger)
    content_list_type = Column(String)
    should_download = Column(Boolean, default=True)
    is_downloaded = Column(Boolean, default=False)
    download_date = Column(BigInteger)
    download_type = Column(String)
    created_at = Column(BigInteger, default=lambda: int(datetime.datetime.now().timestamp()))
    updated_at = Column(BigInteger, default=lambda: int(datetime.datetime.now().timestamp()), onupdate=lambda: int(datetime.datetime.now().timestamp()))
    module_id = Column(String, ForeignKey('modules.id'))
    module = relationship("Module", back_populates="lessons")
    files = relationship("File", back_populates="lesson")
    logs = relationship("Log", back_populates="lesson")

    def to_dict(self, include_module=True, include_files=True):
        result = {
            'katomart_id': self.katomart_id,
            'id': self.id.decode('utf-8') if isinstance(self.id, bytes) else self.id,
            'extra_data': self.extra_data,
            'name': self.name.decode('utf-8') if isinstance(self.name, bytes) else self.name,
            'formatted_name': self.formatted_name.decode('utf-8') if isinstance(self.formatted_name, bytes) else self.formatted_name,
            'order': int(self.order),
            'description': self.description.decode('utf-8') if isinstance(self.description, bytes) else (self.description or ''),
            'is_active': bool(self.is_active),
            'is_locked': bool(self.is_locked),
            'unlocks_at': int(self.unlocks_at) if self.unlocks_at else None,
            'has_drm': bool(self.has_drm),
            'is_listed': bool(self.is_listed),
            'content_list_date': int(self.content_list_date) if self.content_list_date else None,
            'content_list_type': self.content_list_type.decode('utf-8') if isinstance(self.content_list_type, bytes) else self.content_list_type,
            'should_download': bool(self.should_download),
            'is_downloaded': bool(self.is_downloaded),
            'download_date': int(self.download_date) if self.download_date else None,
            'download_type': self.download_type.decode('utf-8') if isinstance(self.download_type, bytes) else self.download_type,
            'created_at': int(self.created_at),
            'updated_at': int(self.updated_at),
            'files': [file.to_dict(include_lesson=False) for file in self.files] if (include_files and self.files) else []
        }

        if include_module:
            result['module'] = self.module.to_dict(include_course=False) if self.module else None  # Prevent recursion
        return result

class File(Base):
    __tablename__ = 'files'
    katomart_id = Column(Integer, primary_key=True)
    id = Column(String)
    extra_data = Column(JSON)
    name = Column(String)
    formatted_name = Column(String)
    order = Column(Integer)
    description = Column(String)
    is_active = Column(Boolean, default=False)
    is_locked = Column(Boolean, default=False)
    should_download = Column(Boolean, default=True)
    unlocks_at = Column(BigInteger)
    has_drm = Column(Boolean, default=False)
    is_decrypted = Column(Boolean, default=False)
    is_downloaded = Column(Boolean, default=False)
    download_date = Column(BigInteger)
    file_size = Column(Integer)
    file_type = Column(String)
    duration = Column(Integer)
    lesson_id = Column(String, ForeignKey('lessons.id'))
    created_at = Column(BigInteger, default=lambda: int(datetime.datetime.now().timestamp()))
    updated_at = Column(BigInteger, default=lambda: int(datetime.datetime.now().timestamp()), onupdate=lambda: int(datetime.datetime.now().timestamp()))
    lesson = relationship("Lesson", back_populates="files")
    logs = relationship("Log", back_populates="file")

    video_notes = relationship("VideoNote", back_populates="file", cascade="all, delete, delete-orphan")
    pdf_annotations = relationship("PdfAnnotation", back_populates="file", cascade="all, delete, delete-orphan")

    def to_dict(self, include_lesson=True, include_video_notes=True, include_pdf_annotations=True):
        result = {
            'katomart_id': self.katomart_id,
            'id': self.id.decode('utf-8') if isinstance(self.id, bytes) else self.id,
            'extra_data': self.extra_data,
            'name': self.name.decode('utf-8') if isinstance(self.name, bytes) else self.name,
            'formatted_name': self.formatted_name.decode('utf-8') if isinstance(self.formatted_name, bytes) else self.formatted_name,
            'order': int(self.order),
            'description': self.description.decode('utf-8') if isinstance(self.description, bytes) else (self.description or ''),
            'is_active': bool(self.is_active),
            'is_locked': bool(self.is_locked),
            'should_download': bool(self.should_download),
            'unlocks_at': int(self.unlocks_at) if self.unlocks_at else None,
            'has_drm': bool(self.has_drm),
            'is_decrypted': bool(self.is_decrypted),
            'is_downloaded': bool(self.is_downloaded),
            'download_date': int(self.download_date) if self.download_date else None,
            'file_size': int(self.file_size),
            'file_type': self.file_type.decode('utf-8') if isinstance(self.file_type, bytes) else self.file_type,
            'duration': int(self.duration) if self.duration else None,
            'created_at': int(self.created_at),
            'updated_at': int(self.updated_at),
            'lesson_id': self.lesson_id,
            'video_notes': [note.to_dict(include_file=False) for note in self.video_notes] if (include_video_notes and self.video_notes) else [],
            'pdf_annotations': [annotation.to_dict(include_file=False) for annotation in self.pdf_annotations] if (include_pdf_annotations and self.pdf_annotations) else [],
            'lesson': self.lesson.to_dict(include_module=False, include_files=False) if (include_lesson and self.lesson) else None,
        }
        return result
    
class VideoNote(Base):
    __tablename__ = 'video_notes'
    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey('files.katomart_id'), nullable=False)
    time = Column(Float, nullable=False)  # Time in seconds
    text = Column(String, nullable=False)
    created_at = Column(BigInteger, default=lambda: int(datetime.datetime.now().timestamp()))
    updated_at = Column(
        BigInteger,
        default=lambda: int(datetime.datetime.now().timestamp()),
        onupdate=lambda: int(datetime.datetime.now().timestamp())
    )

    # Relationship to the File model
    file = relationship("File", back_populates="video_notes")

    def to_dict(self, include_file=True):
        result = {
            'id': self.id,
            'file_id': self.file_id,
            'time': self.time,
            'text': self.text,
            'created_at': int(self.created_at),
            'updated_at': int(self.updated_at)
        }
        if include_file and self.file:
            result['file'] = self.file.to_dict(include_lesson=False, include_video_notes=False, include_pdf_annotations=False)
        return result

class PdfAnnotation(Base):
    __tablename__ = 'pdf_annotations'
    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey('files.katomart_id'), nullable=False)
    annotations = Column(JSON, nullable=False)
    created_at = Column(BigInteger, default=lambda: int(datetime.datetime.now().timestamp()))
    updated_at = Column(
        BigInteger,
        default=lambda: int(datetime.datetime.now().timestamp()),
        onupdate=lambda: int(datetime.datetime.now().timestamp())
    )

    # Relationship to the File model
    file = relationship("File", back_populates="pdf_annotations")

    def to_dict(self, include_file=True):
        result = {
            'id': self.id,
            'file_id': self.file_id,
            'annotations': self.annotations,
            'created_at': int(self.created_at),
            'updated_at': int(self.updated_at)
        }
        if include_file and self.file:
            result['file'] = self.file.to_dict(include_lesson=False, include_video_notes=False, include_pdf_annotations=False)
        return result
