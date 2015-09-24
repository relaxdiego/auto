from tflib.step import Step


class GetIndex(Step):

    def execute(self, app):
        self.log.info("GET /")
        self.response = app.get('/')

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
