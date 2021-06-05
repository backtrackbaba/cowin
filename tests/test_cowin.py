import copy
import json
import os

from cowin_api import CoWinAPI
from cowin_api.constants import Constants
from cowin_api.utils import filter_centers


def get_sample_response() -> dict:
    with open(os.path.join('tests', 'data', 'response.json'), 'r') as f:
        data = json.load(f)
    return data


def get_final_filters(user_filters: dict):
    final_filters = copy.copy(Constants.default_filters)
    final_filters.update(user_filters)
    return final_filters


def get_sessions_count(centers: dict) -> int:
    sessions = 0
    for center in centers.get('centers'):
        sessions += len(center.get('sessions'))
    return sessions


def test_get_states():
    cowin = CoWinAPI()
    states = cowin.get_states()

    assert isinstance(states, dict)
    assert states.get('states')[0].get('state_id') == 1


def test_get_districts():
    cowin = CoWinAPI()
    districts = cowin.get_districts("21")

    assert isinstance(districts, dict)
    assert districts.get('districts')[0].get('district_id') == 391


def test_get_availability_by_district():
    cowin = CoWinAPI()
    availability = cowin.get_availability_by_district("395")

    assert isinstance(availability, dict)
    assert isinstance(availability.get('centers'), list)


def test_get_availability_by_pincode():
    cowin = CoWinAPI()
    availability = cowin.get_availability_by_pincode("400080")

    assert isinstance(availability, dict)
    assert isinstance(availability.get('centers'), list)


def test_min_age_limit_filter():
    cowin = CoWinAPI()
    availability = cowin.get_availability_by_district("395", date="03-05-2021")

    assert isinstance(availability, dict)
    assert isinstance(availability.get('centers'), list)


def test_age_limit_filter():
    filters = {'min_age_limit': 45}
    availability = filter_centers(get_sample_response(), get_final_filters(filters))

    assert len(availability.get('centers')) == 3
    assert get_sessions_count(availability) == 5


def test_fee_type_filter():
    filters = {'fee_type': "Free"}
    availability = filter_centers(get_sample_response(), get_final_filters(filters))

    assert len(availability.get('centers')) == 2
    assert get_sessions_count(availability) == 7

    filters = {'fee_type': "Paid"}
    availability = filter_centers(get_sample_response(), get_final_filters(filters))

    assert len(availability.get('centers')) == 2
    assert get_sessions_count(availability) == 5


def test_availability_filter():
    filters = {'available_capacity': 20}
    availability = filter_centers(get_sample_response(), get_final_filters(filters))

    assert len(availability.get('centers')) == 2
    assert get_sessions_count(availability) == 6

    filters = {'available_capacity_dose1': 10}
    availability = filter_centers(get_sample_response(), get_final_filters(filters))

    assert len(availability.get('centers')) == 2
    assert get_sessions_count(availability) == 5

    filters = {'available_capacity_dose2': 10}
    availability = filter_centers(get_sample_response(), get_final_filters(filters))

    assert len(availability.get('centers')) == 2
    assert get_sessions_count(availability) == 7


def test_vaccine_filter():
    filters = {'vaccine': ['COVAXIN']}
    availability = filter_centers(get_sample_response(), get_final_filters(filters))

    assert len(availability.get('centers')) == 3
    assert get_sessions_count(availability) == 3

    filters = {'vaccine': ['COVISHIELD']}
    availability = filter_centers(get_sample_response(), get_final_filters(filters))

    assert len(availability.get('centers')) == 3
    assert get_sessions_count(availability) == 5

    filters = {'vaccine': ['Sputnik V']}
    availability = filter_centers(get_sample_response(), get_final_filters(filters))

    assert len(availability.get('centers')) == 3
    assert get_sessions_count(availability) == 4

    filters = {'vaccine': ['Sputnik V', 'COVISHIELD']}
    availability = filter_centers(get_sample_response(), get_final_filters(filters))

    assert len(availability.get('centers')) == 4
    assert get_sessions_count(availability) == 9

    filters = {'vaccine': ['COVAXIN', 'COVISHIELD']}
    availability = filter_centers(get_sample_response(), get_final_filters(filters))

    assert len(availability.get('centers')) == 4
    assert get_sessions_count(availability) == 8

    filters = {'vaccine': ['Sputnik V', 'COVAXIN']}
    availability = filter_centers(get_sample_response(), get_final_filters(filters))

    assert len(availability.get('centers')) == 3
    assert get_sessions_count(availability) == 7


def test_no_filter():
    availability = filter_centers(get_sample_response(), get_final_filters({}))

    assert len(availability.get('centers')) == 4
    assert get_sessions_count(availability) == 12
