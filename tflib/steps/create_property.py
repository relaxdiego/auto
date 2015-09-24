import json

from tflib.step import Step


class CreateProperty(Step):

    def __init__(self, owner, desc):
        self.args = {}
        self.args['owner'] = owner
        self.args['desc'] = desc

    def execute(self, app):
        self.app = app
        self.log.info("POST /properties")
        self.response = app.post('/properties',
                                 data=json.dumps(self.args),
                                 content_type='application/json')

        self.log.info("Received response: %r" % self.response)

        try:
            self.record = json.loads(self.response.data)
        except ValueError:
            return None

        return self.record.get('id', None)

    def undo(self):
        path = '/properties/%s' % self.record['id']
        self.log.info("DELETE %s" % path)
        response = self.app.delete(path)

        if response.status_code == 200:
            self.log.info("Received response: %r" % response.status)
        else:
            self.log.error("Undo FAILED. Received: %r" % response.data)

    def created_expectation(self):
        resp = self.response

        if resp.status_code != 200:
            msg = "Expected the property to be created but got the " \
                  "following response instead: %r" % resp
            return False, msg

        try:
            record = json.loads(resp.data)
        except ValueError:
            msg = "Expected a valid JSON string to be returned but " \
                  "got the following instead: '%s'" % resp.data
            return False, msg

        expected = ['id', 'owner', 'desc']
        actual = record.keys()

        if set(expected) != set(actual):
            msg = "Expected the fields %r to be returned but got " \
                  "the following instead: %r" % (expected, actual)
            return False, msg

        if self.args != {k: v for k, v in record.items() if k != 'id'}:
            msg = "Expected property to have the following values '%r'" \
                  " but got the following instead: '%r'" % (self.args, record)
            return False, msg

        return True, ""
