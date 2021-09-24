import copy
import json
import os

import pytest
import responses

from cowin_api import CoWinAPI
from cowin_api.constants import Constants
from cowin_api.utils import today, filter_centers


def get_test_data(file_name):
    with open(os.path.join(Constants.tests_data_dir, file_name), 'r') as f:
        return json.load(f)


def get_final_filters(user_filters: dict):
    final_filters = copy.copy(Constants.default_filters)
    final_filters.update(user_filters)
    return final_filters


def get_sessions_count(centers: dict) -> int:
    sessions = 0
    for center in centers.get('centers'):
        sessions += len(center.get('sessions'))
    return sessions


@pytest.fixture
def init_data():
    states_data = get_test_data('states_responses.json')
    districts_data = get_test_data('districts_responses.json')
    availability_by_district_data = get_test_data('availability_by_district_responses.json')
    availability_by_pincode_data = get_test_data('availability_by_pincode_responses.json')
    centers_by_lat_long = get_test_data('centers_by_lat_long_responses.json')

    responses.add(
        responses.Response(
            method='GET',
            url=f"{Constants.districts_list_url}/21",
            json=districts_data,
            status=200
        )
    )

    responses.add(
        responses.Response(
            method='GET',
            url=f"{Constants.availability_by_district_url}?district_id=395&date={today()}",
            json=availability_by_district_data,
            status=200
        )
    )

    responses.add(
        responses.Response(
            method='GET',
            url=Constants.states_list_url,
            json=states_data,
            status=200
        )
    )

    responses.add(
        responses.Response(
            method='GET',
            url=f"{Constants.availability_by_pin_code_url}?pincode=400080&date={today()}",
            json=availability_by_pincode_data,
            status=200
        )
    )

    responses.add(
        responses.Response(
            method='GET',
            url=f"{Constants.centers_by_lat_long}?lat=18.93&long=72.82",
            json=centers_by_lat_long,
            status=200
        )
    )


@responses.activate
def test_get_states(init_data):
    cowin = CoWinAPI()
    states = cowin.get_states()

    assert isinstance(states, dict)
    assert states.get('states')[0].get('state_id') == 1


@responses.activate
def test_get_districts(init_data):
    cowin = CoWinAPI()
    districts = cowin.get_districts("21")

    assert isinstance(districts, dict)
    assert districts.get('districts')[0].get('district_id') == 391


@responses.activate
def test_get_availability_by_district(init_data):
    cowin = CoWinAPI()
    availability = cowin.get_availability_by_district("395")

    assert isinstance(availability, dict)
    assert isinstance(availability.get('centers'), list)


@responses.activate
def test_get_availability_by_pincode(init_data):
    cowin = CoWinAPI()
    availability = cowin.get_availability_by_pincode("400080")

    assert isinstance(availability, dict)
    assert isinstance(availability.get('centers'), list)


@responses.activate
def test_get_centers_by_lat_long(init_data):
    cowin = CoWinAPI()
    lat = 18.93
    long = 72.82
    availability = cowin.get_centers_by_lat_long(lat, long)

    assert isinstance(availability, dict)
    assert isinstance(availability.get('centers'), list)


def test_age_limit_filter():
    filters = {'min_age_limit': 45}
    availability = filter_centers(get_test_data('availability_by_district_responses.json'), get_final_filters(filters))

    assert len(availability.get('centers')) == 3
    assert get_sessions_count(availability) == 5


def test_fee_type_filter():
    filters = {'fee_type': "Free"}
    availability = filter_centers(get_test_data('availability_by_district_responses.json'), get_final_filters(filters))

    assert len(availability.get('centers')) == 2
    assert get_sessions_count(availability) == 7

    filters = {'fee_type': "Paid"}
    availability = filter_centers(get_test_data('availability_by_district_responses.json'), get_final_filters(filters))

    assert len(availability.get('centers')) == 2
    assert get_sessions_count(availability) == 5


def test_availability_filter():
    filters = {'available_capacity': 20}
    availability = filter_centers(get_test_data('availability_by_district_responses.json'), get_final_filters(filters))

    assert len(availability.get('centers')) == 2
    assert get_sessions_count(availability) == 6

    filters = {'available_capacity_dose1': 10}
    availability = filter_centers(get_test_data('availability_by_district_responses.json'), get_final_filters(filters))

    assert len(availability.get('centers')) == 2
    assert get_sessions_count(availability) == 5

    filters = {'available_capacity_dose2': 10}
    availability = filter_centers(get_test_data('availability_by_district_responses.json'), get_final_filters(filters))

    assert len(availability.get('centers')) == 2
    assert get_sessions_count(availability) == 7


def test_vaccine_filter():
    filters = {'vaccine': ['COVAXIN']}
    availability = filter_centers(get_test_data('availability_by_district_responses.json'), get_final_filters(filters))

    assert len(availability.get('centers')) == 3
    assert get_sessions_count(availability) == 3

    filters = {'vaccine': ['COVISHIELD']}
    availability = filter_centers(get_test_data('availability_by_district_responses.json'), get_final_filters(filters))

    assert len(availability.get('centers')) == 3
    assert get_sessions_count(availability) == 5

    filters = {'vaccine': ['Sputnik V']}
    availability = filter_centers(get_test_data('availability_by_district_responses.json'), get_final_filters(filters))

    assert len(availability.get('centers')) == 3
    assert get_sessions_count(availability) == 4

    filters = {'vaccine': ['Sputnik V', 'COVISHIELD']}
    availability = filter_centers(get_test_data('availability_by_district_responses.json'), get_final_filters(filters))

    assert len(availability.get('centers')) == 4
    assert get_sessions_count(availability) == 9

    filters = {'vaccine': ['COVAXIN', 'COVISHIELD']}
    availability = filter_centers(get_test_data('availability_by_district_responses.json'), get_final_filters(filters))

    assert len(availability.get('centers')) == 4
    assert get_sessions_count(availability) == 8

    filters = {'vaccine': ['Sputnik V', 'COVAXIN']}
    availability = filter_centers(get_test_data('availability_by_district_responses.json'), get_final_filters(filters))

    assert len(availability.get('centers')) == 3
    assert get_sessions_count(availability) == 7


def test_no_filter():
    availability = filter_centers(get_test_data('availability_by_district_responses.json'), get_final_filters({}))

    assert len(availability.get('centers')) == 4
    assert get_sessions_count(availability) == 12
