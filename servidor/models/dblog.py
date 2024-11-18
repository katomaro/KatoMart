import datetime
from sqlalchemy import Column, Integer, ForeignKey, Text, Enum, BigInteger, String
from sqlalchemy.orm import relationship
from . import Base

class Log(Base):
    __tablename__ = 'logs'
    
    id = Column(String, primary_key=True)
    event_type = Column(Enum(
        'application_start',
        'application_stop',
        'update_config',
        'phone_home',
        'informational',
        'warning',
        'authentication',
        'log_out',
        'system_error',
        'course_list',
        'module_list',
        'lesson_list',
        'file_list',
        'file_download',
        'file_upload',
        'download_error',
        'download_management',
        'upload_error',
        'catch_all_error',
        name='event_types'
    ), nullable=False)
    
    message = Column(Text, nullable=True)
    created_at = Column(BigInteger, default=lambda: int(datetime.datetime.utcnow().timestamp()))
    
    # Foreign keys
    platform_auth_id = Column(Integer, ForeignKey('platform_auths.id'))
    platform_id = Column(Integer, ForeignKey('platforms.id'))
    course_id = Column(String, ForeignKey('courses.id'))
    module_id = Column(String, ForeignKey('modules.id'))
    lesson_id = Column(String, ForeignKey('lessons.id'))
    file_id = Column(String, ForeignKey('files.id'))
    
    # Relationships
    platform = relationship("Platform", back_populates="logs")
    platform_auth = relationship("PlatformAuth", back_populates="logs")
    course = relationship("Course", back_populates="logs")
    module = relationship("Module", back_populates="logs")
    lesson = relationship("Lesson", back_populates="logs")
    file = relationship("File", back_populates="logs")
    
    def __repr__(self):
        return f"<Log(event_type={self.event_type}, message={self.message}, created_at={self.created_at}, platform_id={self.platform_id}, platform_auth_id={self.platform_auth_id}, course_id={self.course_id}, module_id={self.module_id}, lesson_id={self.lesson_id}, file_id={self.file_id})>"
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'event_type': str(self.event_type),
            'message': self.message.decode('utf-8') if isinstance(self.message, bytes) else self.message,
            'created_at': int(self.created_at),
            'platform_id': int(self.platform_id) if self.platform_id else None,
            'platform_auth_id': int(self.platform_auth_id) if self.platform_auth_id else None,
            'course_id': str(self.course_id) if self.course_id else None,
            'module_id': str(self.module_id) if self.module_id else None,
            'lesson_id': str(self.lesson_id) if self.lesson_id else None,
            'file_id': str(self.file_id) if self.file_id else None,
            # Add nested relationships if needed
            'platform': self.platform.to_dict() if self.platform else None,
            'platform_auth': self.platform_auth.to_dict() if self.platform_auth else None,
            'course': self.course.to_dict() if self.course else None,
            'module': self.module.to_dict() if self.module else None,
            'lesson': self.lesson.to_dict() if self.lesson else None,
            'file': self.file.to_dict() if self.file else None
        }
