from tflib.test_case import TestCase
from tflib.steps.create_user import CreateUser


class TestCreateUser(TestCase):

    def steps(self):
        self.step(CreateUser(name='Kung Fury'), expect='created')
