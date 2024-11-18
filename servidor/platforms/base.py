from abc import ABC, abstractmethod
import threading
import time

class PlatformScraper(ABC):
    def __init__(self, auth_data, scraper=None):
        self.auth_data = auth_data
        self.scraper = scraper
        self.pause_event = threading.Event()
        self.stop_event = threading.Event()
        self.progress = 0  # For progress tracking
        self.max_progress = 0  # For progress tracking

        # Queues for managing downloads
        self.normal_queue = []
        self.priority_queue = []

    @abstractmethod
    def login(self):
        pass

    @abstractmethod
    def get_course_data(self):
        pass

    def start_downloads(self):
        """Start processing the download queues."""
        self.pause()

    # Queue management methods
    def add_to_normal_queue(self, file_info):
        """Add a file to the normal download queue."""
        self.normal_queue.append(file_info)

    def add_to_priority_queue(self, file_info):
        """Add a file to the priority download queue."""
        self.priority_queue.append(file_info)
        # Remove it from the normal queue to prevent duplicates
        self.remove_from_normal_queue(file_info)

    def remove_from_normal_queue(self, file_info):
        """Remove a file from the normal queue."""
        self.normal_queue = [item for item in self.normal_queue if not self.compare_file_info(item, file_info)]

    def remove_from_priority_queue(self, file_info):
        """Remove a file from the priority queue."""
        self.priority_queue = [item for item in self.priority_queue if not self.compare_file_info(item, file_info)]

    def demote_from_priority_queue(self, file_info):
        """
        Remove an item from the priority queue and add it back to the normal queue.
        """
        self.remove_from_priority_queue(file_info)
        self.add_to_normal_queue(file_info)

    def compare_file_info(self, item1, item2):
        """
        Helper method to compare two file_info dictionaries.
        Override this method if the comparison criteria differ.
        """
        return item1.get('id') == item2.get('id')

    def enqueue_files(self, files):
        """
        Add multiple files to the normal download queue.

        Parameters:
        - files: A list of file_info dictionaries.
        """
        for file_info in files:
            self.add_to_normal_queue(file_info)

    def pause(self):
        self.pause_event.set()

    def resume(self):
        self.pause_event.clear()

    def stop(self):
        self.stop_event.set()

    def is_paused(self):
        return self.pause_event.is_set()

    def is_stopped(self):
        return self.stop_event.is_set()

    def close(self):
        if self.scraper:
            self.scraper.close()
