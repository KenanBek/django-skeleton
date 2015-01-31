import uuid

from system import models

''' Event Logger '''


class EventLogger:
    def __init__(self, title_of_event):
        self.uuid = str(uuid.uuid4())
        self.title = title_of_event

        event = models.Event()
        event.uuid = self.uuid
        event.title = self.title
        event.save()

        event.identifier = "{} {}".format(event.title, event.pk)
        event.save()

        self.event = event

    def new_log(self, level, text, *args):
        log = models.Log()
        log.event = self.event
        log.level = level
        log.text = text.format(*args)
        log.save()

    def new_debug_log(self, text, *args):
        self.new_log(models.LOG_LEVEL_DEBUG, text, *args)

    def new_info_log(self, text, *args):
        self.new_log(models.LOG_LEVEL_INFO, text, *args)

    def new_warning_log(self, text, *args):
        self.new_log(models.LOG_LEVEL_WARNING, text, *args)

    def new_error_log(self, text, *args):
        self.new_log(models.LOG_LEVEL_ERROR, text, *args)

    def new_critical_log(self, text, *args):
        self.new_log(models.LOG_LEVEL_CRITICAL, text, *args)