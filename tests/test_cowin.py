import json
import os

from cowin_api import CoWinAPI
from cowin_api.utils import filter_centers

def get_data():
    with open(os.path.join('tests', 'sample_response_for_testing.json'), 'r') as f:
        data = json.load(f)
    return data

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
    availability = filter_centers(get_data(), {'min_age_limit': 18})

    assert isinstance(availability, dict)
    assert isinstance(availability.get('centers'), list)
    assert len(availability.get('centers')) == 1


def test_vaccine_filter():
    availability = filter_centers(get_data(), {'vaccine': 'COVAXIN'})

    assert isinstance(availability, dict)
    assert isinstance(availability.get('centers'), list)
    assert sum([len(center.get('sessions')) \
                for center in availability.get('centers')]) == 10


def test_availability_filter():
    availability = filter_centers(get_data(), {'available_capacity': 1})

    assert isinstance(availability, dict)
    assert isinstance(availability.get('centers'), list)
    assert sum([len(center.get('sessions')) \
                for center in availability.get('centers')]) == 37


def test_fee_type_filter():
    availability = filter_centers(get_data(), {'fee_type': 'Paid'})

    assert isinstance(availability, dict)
    assert isinstance(availability.get('centers'), list)
    assert len(availability.get('centers')) == 0


def test_fee_type_filter_2():
    availability = filter_centers(get_data(), {'fee_type': 'Free'})

    assert isinstance(availability, dict)
    assert isinstance(availability.get('centers'), list)
    assert len(availability.get('centers')) == 47


def test_multiple_filter():
    availability = filter_centers(get_data(),
                                 {'vaccine': 'COVAXIN',
                                  'available_capacity': 1})

    assert isinstance(availability, dict)
    assert isinstance(availability.get('centers'), list)
    assert sum([len(center.get('sessions')) \
                for center in availability.get('centers')]) == 7


def test_multiple_filter_2():
    availability = filter_centers(get_data(),
                                 {'vaccine': ['COVAXIN', 'COVISHIELD'],
                                  'available_capacity': 5})

    assert isinstance(availability, dict)
    assert isinstance(availability.get('centers'), list)
    assert sum([len(center.get('sessions')) \
                for center in availability.get('centers')]) == 32
