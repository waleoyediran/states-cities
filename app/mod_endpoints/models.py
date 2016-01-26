from parse_rest.datatypes import Object
from parse_rest.query import QueryResourceDoesNotExist
from app.mod_endpoints.exceptions import InvalidAPIUsage


class State(Object):
    def as_dict(self):
        return {
            'name': self.name,
            'capital': self.cap_city,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'minLat': self.min_latitude,
            'minLong': self.min_longitude,
            'maxLat': self.max_latitude,
            'maxLong': self.max_longitude
        }

    @classmethod
    def find_by_name_or_code(cls,state_name_or_code):
        try:
            if len(state_name_or_code) == 2:
                state = State.Query.get(state_code=state_name_or_code.upper())
            elif len(state_name_or_code) > 2:
                state = State.Query.get(name=state_name_or_code.title())
            return state
        except QueryResourceDoesNotExist, e:
            raise InvalidAPIUsage("State with state name or code '{}' does not exist".format(state_name_or_code), status_code=404)


def get_all_states():
    return [ state.as_dict() for state in State.Query.all() ]


def get_one_state(state_name_or_code):
    _state_ = State.find_by_name_or_code(state_name_or_code)
    # print _state_
    return _state_.as_dict()

class LGA(Object):
    def as_dict(self):
        return {
            'name': self.name
        }

    @classmethod
    def find_state_cities(cls,state_name_or_code):
        _state_ = State.find_by_name_or_code(state_name_or_code)
        return [ lga.as_dict() for lga in LGA.Query.filter( state=_state_, city=True ) ]

    @staticmethod
    def get_all_lgas_with_state_name(state_name):
        result_set = []
        state_result = State.Query.get(name=state_name)
        print state_result.objectId
        lgas = LGA.Query.filter(state=state_result)
        for lga in lgas:
            result_set.append(lga.as_dict())
        return result_set

    @staticmethod
    def get_all_lgas(state_name_or_code):
        _state_ = State.find_by_name_or_code(state_name_or_code)
        return [ lga.as_dict() for lga in LGA.Query.filter(state=_state_) ]

    @staticmethod
    def get_all_cities(state_name_or_code):
        return LGA.find_state_cities(state_name_or_code)

