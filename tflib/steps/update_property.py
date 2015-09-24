import json

from tflib.step import Step


class UpdateProperty(Step):

    def __init__(self, property_id, **kwargs):
        self.property_id = property_id
        self.args = kwargs

    def execute(self, app):
        self.app = app
        path = "/properties/%s" % self.property_id

        self.log.info("Getting initial state")
        response = app.get(path)
        record = json.loads(response.data)
        self.initial = {k: v for k, v in record.items() if k != 'id'}

        self.log.info("Initial state: %r" % response.data)

        self.log.info("PUT %s" % path)
        self.response = app.put(path,
                                data=json.dumps(self.args),
                                content_type='application/json')

        self.log.info("Received response: %r" % self.response)

        self.log.info("Updated state: %r" % self.response.data)

        try:
            self.record = json.loads(self.response.data)
        except ValueError:
            return None

        return self.record

    def undo(self):
        path = '/properties/%s' % self.property_id
        self.log.info("PUT %s" % path)
        response = self.app.put(path, data=json.dumps(self.initial),
                                content_type='application/json')

        if response.status_code == 200:
            self.log.info("Received response: %r" % response.status)
            self.log.info("State reverted to: %r" % response.data)
        else:
            self.log.error("Undo FAILED. Received: %r" % response.data)

    def updated_expectation(self):
        resp = self.response

        if resp.status_code != 200:
            msg = "Expected the property to be updated but got the " \
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

        actual = {k: v for k, v in record.items() if k in self.args.keys()}
        if self.args != actual:
            msg = "Expected property to have the following values '%r'" \
                  " but got the following instead: '%r'" % (self.args, record)
            return False, msg

        return True, ""
