from tflib.test_case import TestCase
from tflib.steps.get_index import GetIndex


class TestIndex(TestCase):

    def steps(self):
        self.step(GetIndex(), expect='success')
