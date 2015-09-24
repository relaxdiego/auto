import json

from tflib.step import Step


class GetProperty(Step):

    def __init__(self, property_id):
        self.property_id = property_id

    def execute(self, app, ):
        path = "/properties/%s" % self.property_id

        self.log.info("GET %s" % path)
        self.response = app.get(path)

        self.log.info("Received response: %r" % self.response)
        return self.response.status_code

    def success_expectation(self):
        resp = self.response
        success = resp.status_code == 200

        if success:
            return True, ""
        else:
            msg = "Expected an HTTP 200 reponse but got the following " \
                  "response instead: %r" % resp
            return False, msg

    def specific_owner_expectation(self, owner_id):
        success, msg = self.success_expectation()

        if not success:
            return False, msg

        record = json.loads(self.response.data)

        if record['owner'] != owner_id:
            msg = "Expected owner to be %s but got %s instead" \
                  % (owner_id, record['owner_id'])
            return False, msg
        else:
            return True, ""
