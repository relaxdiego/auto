from mock import Mock

from tflib.steps.get_index import GetIndex


class TestGetIndex:

    def test_success_expectation__met(self):
        mock_app = Mock()
        mock_app.get.return_value.status_code = 200

        step = GetIndex()
        step.execute(mock_app)

        success, msg = step.success_expectation()

        assert success
        assert msg == ""

    def test_success_expectation__not_met(self):
        mock_app = Mock()
        mock_app.get.return_value.status_code = 400

        step = GetIndex()
        step.execute(mock_app)

        success, msg = step.success_expectation()

        assert success is False
        assert msg != ""
