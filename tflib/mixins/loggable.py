import logging


class LoggableMixin:

    @property
    def log(self):
        attr = "_log_"

        if not hasattr(self, attr):
            setattr(self, attr, logging.getLogger(self.__class__.__name__))

        return getattr(self, attr)
