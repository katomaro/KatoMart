class Product:
    def __init__(self, product_id, name, progress):
        self.product_id = product_id
        self.name = name
        self.progress = progress
        self.modules = []

    def add_module(self, module):
        self.modules.append(module)
        self.update_progress()

    def remove_module(self, module_id):
        self.modules = [module for module in self.modules if module.id != module_id]
        self.update_progress()

    def update_progress(self):
        if self.modules:
            self.progress = sum(module.progress for module in self.modules) / len(self.modules)

    def to_dict(self):
        return {
            'product_id': self.product_id,
            'name': self.name,
            'progress': self.progress,
            'modules': [module.to_dict() for module in self.modules]
        }

class Module:
    def __init__(self, module_id, name, progress):
        self.id = module_id
        self.name = name
        self.progress = progress
        self.lessons = []

    def add_lesson(self, lesson):
        self.lessons.append(lesson)
        self.update_progress()

    def remove_lesson(self, lesson_id):
        self.lessons = [lesson for lesson in self.lessons if lesson.id != lesson_id]
        self.update_progress()

    def update_progress(self):
        if self.lessons:
            self.progress = sum(lesson.progress for lesson in self.lessons) / len(self.lessons)

    def to_dict(self):
        return {
            'name': self.name,
            'progress': self.progress,
            'lessons': [lesson.to_dict() for lesson in self.lessons]
        }

class Lesson:
    def __init__(self, lesson_id, name):
        self.id = lesson_id
        self.name = name
        self.progress = 0.0
        self.has_text = False
        self.text = ''
        self.has_video = False
        self.videos = []
        self.has_audio = False
        self.audios = []
        self.has_external_links = False
        self.external_links = []
        self.has_attachments = False
        self.attachments = []

    def set_text(self, text):
        self.text = text
        self.has_text = True

    def update_progress(self):
        video_progress = sum(video.progress for video in self.videos) / len(self.videos) if self.has_video else 100.0
        audio_progress = sum(audio.progress for audio in self.audios) / len(self.audios) if self.has_audio else 100.0
        attachments_progress = sum(attachment.progress for attachment in self.attachments) / len(self.attachments) if self.has_attachments else 100.0
        self.progress = (video_progress + audio_progress + attachments_progress) / 3

    def add_video(self, video):
        self.videos.append(video)
        self.has_video = True
        self.update_progress()
    
    def remove_video(self, video_id):
        self.videos = [video for video in self.videos if video.id != video_id]
        self.has_video = bool(self.videos)
        self.update_progress()
    
    def add_audio(self, audio):
        self.audios.append(audio)
        self.has_audio = True
        self.update_progress()
    
    def remove_audio(self, audio_id):
        self.audios = [audio for audio in self.audios if audio.id != audio_id]
        self.has_audio = bool(self.audios)
        self.update_progress()
    
    def add_external_link(self, external_link):
        self.external_links.append(external_link)
        self.has_external_links = True
    
    def remove_external_link(self, external_link):
        self.external_links = [link for link in self.external_links if link != external_link]
        self.has_external_links = bool(self.external_links)

    def add_attachment(self, attachment):
        self.attachments.append(attachment)
        self.has_attachments = True
        self.update_progress()

    def remove_attachment(self, attachment_id):
        self.attachments = [attachment for attachment in self.attachments if attachment.id != attachment_id]
        self.has_attachments = bool(self.attachments)
        self.update_progress()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'progress': self.progress,
            'has_text': self.has_text,
            'text': self.text,
            'has_video': self.has_video,
            'videos': [video.to_dict() for video in self.videos],
            'has_audio': self.has_audio,
            'audios': [audio.to_dict() for audio in self.audios],
            'has_external_links': self.has_external_links,
            'external_links': self.external_links,
            'has_attachments': self.has_attachments,
            'attachments': [attachment.to_dict() for attachment in self.attachments]
        }

class Video:
    def __init__(self, video_id,
                 name,
                 is_vod,
                 url):

        self.id = video_id
        self.name = name
        self.progress = 0.0
        self.finished = False
        self.is_vod = is_vod
        self.total_segments = 0
        self.segments = []
        self.downloaded_segments = 0
        self.url = url

    def add_segment(self, segment_url):
        self.segments.append(segment_url)
        self.total_segments += 1
    
    def update_progress(self):
        self.downloaded_segments += 1
        self.progress = self.downloaded_segments / self.total_segments

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'progress': self.progress,
            'finished': self.finished,
            'is_vod': self.is_vod,
            'total_segments': self.total_segments,
            'downloaded_segments': self.downloaded_segments,
            'url': self.url
        }

class Audio:
    def __init__(self, audio_id, name, url):
        self.id = audio_id
        self.name = name
        self.progress = 0.0
        self.finished = False
        self.url = url

    def update_progress(self):
        self.progress = 100.0

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'progress': self.progress,
            'finished': self.finished,
            'url': self.url
        }

class Attachment:
    def __init__(self, attachment_id, name, url):
        self.id = attachment_id
        self.name = name
        self.progress = 0.0
        self.finished = False
        self.url = url

    def update_progress(self):
        self.progress = 100.0

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'progress': self.progress,
            'finished': self.finished,
            'url': self.url
        }
