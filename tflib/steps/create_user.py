import json

from tflib.step import Step


class CreateUser(Step):

    def __init__(self, name):
        self.args = {}
        self.args['name'] = name

    def execute(self, app):
        self.app = app
        self.log.info("POST /users")
        self.response = app.post('/users',
                                 data=json.dumps(self.args),
                                 content_type='application/json')

        self.log.info("Received response: %r" % self.response)

        try:
            self.record = json.loads(self.response.data)
        except ValueError:
            return None

        return self.record.get('id', None)

    def undo(self):
        path = '/users/%s' % self.record['id']
        self.log.info("DELETE %s" % path)
        response = self.app.delete(path)

        if response.status_code == 200:
            self.log.info("Received response: %r" % response.status)
        else:
            self.log.error("Undo FAILED. Received: %r" % response.data)

    def created_expectation(self):
        resp = self.response

        if resp.status_code != 200:
            msg = "Expected the user to be created but got the " \
                  "following response instead: %r" % resp
            return False, msg

        try:
            record = json.loads(resp.data)
        except ValueError:
            msg = "Expected a valid JSON string to be returned but " \
                  "got the following instead: '%s'" % resp.data
            return False, msg

        expected = ['id', 'name']
        actual = record.keys()

        if set(expected) != set(actual):
            msg = "Expected the fields %r to be returned but got " \
                  "the following instead: %r" % (expected, actual)
            return False, msg

        if self.args != {k: v for k, v in record.items() if k != 'id'}:
            msg = "Expected user to have the following values '%r'" \
                  " but got the following instead: '%r'" % (self.args, record)
            return False, msg

        return True, ""
