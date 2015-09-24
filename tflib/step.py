from tflib.mixins.loggable import LoggableMixin


class Step(object, LoggableMixin):

    def get_expectation(self, name):
        return getattr(self, "%s_expectation" % name)

    def undo(self):
        self.log.info("Nothing to undo")
