from tflib.test_case import TestCase
from tflib.steps.create_user import CreateUser
from tflib.steps.create_property import CreateProperty
from tflib.steps.get_property import GetProperty
from tflib.steps.update_property import UpdateProperty


class TestCreateUser(TestCase):

    def steps(self):
        usr1_id = self.step(CreateUser(name='Kung Fury'),
                            expect='created')

        usr2_id = self.step(CreateUser(name='Hackerman'),
                            expect='created')

        prop_id = self.step(CreateProperty(owner=usr1_id,
                                           desc='Miami'),
                            expect='created')

        self.step(UpdateProperty(property_id=prop_id,
                                 owner=usr2_id),
                  expect='updated')

        self.step(GetProperty(property_id=prop_id),
                  expect='specific_owner',
                  owner_id=usr2_id)
