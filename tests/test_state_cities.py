import json
import unittest

from mock import patch

import app as state_cities
from app.mod_endpoints.exceptions import InvalidAPIUsage


ABIA_MOCK = {
    "minLat": 4.810874, "name": "Abia", "capital": "Umuahia", "latitude": 5.430892099999999,
    "minLong": 7.150823, "maxLat": 6.0191921, "longitude": 7.524724300000001, "maxLong": 7.9630091
}


def get_all_states_mock():
    """Get mock state list"""
    return json.load(open('tests/fixture/states.json'))


def get_one_state_mock(state_name_or_code):
    """Create a Mock get_one_state function"""
    if state_name_or_code == 'abia':
        return ABIA_MOCK
    else:
        raise InvalidAPIUsage("State with state name or code '{}' does not exist".format(state_name_or_code),
                              status_code=404)


@patch('app.mod_endpoints.models.get_all_states', get_all_states_mock)
@patch('app.mod_endpoints.models.get_one_state', get_one_state_mock)
class StateCitiesTestCase(unittest.TestCase):

    def setUp(self):
        state_cities.app.config['TESTING'] = True
        self.app = state_cities.app.test_client()

    def test_get_all_states(self):
        """Test getting all states"""
        result = self.app.get('/api/v1/states')
        self.assertEqual(result.status_code, 200)

        states = json.loads(result.data)
        self.assertEqual(len(states), 37)
        self.assertDictEqual(states[0], ABIA_MOCK)

    def test_get_one_state_by_name(self):
        """Test Get state by name"""
        result = self.app.get('/api/v1/state/abia')
        self.assertEqual(result.status_code, 200)

        state = json.loads(result.data)
        self.assertDictEqual(state, ABIA_MOCK)

    def test_invalid_state(self):
        """Test Getting Invalid State"""
        result = self.app.get('/api/v1/state/yaba')
        self.assertEqual(result.status_code, 404)


if __name__ == '__main__':
    unittest.main()
