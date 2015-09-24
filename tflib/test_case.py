import inspect

import app
from tflib.mixins.loggable import LoggableMixin


class TestCase(object, LoggableMixin):

    def setup(self):
        self.log.info("======= START =======")
        self.undo_stack = []
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()

    def teardown(self):
        self.log.info("Test case completed. Undoing changes")
        for step in self.undo_stack[::-1]:
            self.log.info("Undoing step: %s" % step.__class__.__name__)
            step.undo()

    def step(self, step, expect, **expect_kwargs):
        if inspect.isclass(step):
            step = step()

        self.log.info("Executing step: %s" % step.__class__.__name__)

        result = step.execute(self.app)
        self.log.info("Step returned result: %r" % result)

        self.undo_stack.append(step)

        self.log.info("Validating expectation '%s'" % expect)
        expectation = step.get_expectation(expect)
        expected, failure_message = expectation(**expect_kwargs)

        if expected:
            self.log.info("Expectation met")
        else:
            self.log.error("Expectation not met. %s" % failure_message)

        assert expected, failure_message
        return result
