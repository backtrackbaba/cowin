from cowin_api import CoWinAPI
from cowin_api.constants import Vaccine, Dose, Fees


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
    availability = cowin.get_availability_by_district("395", date="03-05-2021", min_age_limit=18)

    assert isinstance(availability, dict)
    assert isinstance(availability.get('centers'), list)


def test_vaccine_filter():
    cowin = CoWinAPI()
    availability = cowin.get_availability_by_district("395", date="03-05-2021", vaccine=Vaccine.COVAXIN)

    assert isinstance(availability, dict)
    assert isinstance(availability.get('centers'), list)


def test_dose_filter():
    cowin = CoWinAPI()
    availability = cowin.get_availability_by_district("395", date="03-05-2021", dose=Dose.FIRST)

    assert isinstance(availability, dict)
    assert isinstance(availability.get('centers'), list)


def test_fees_filter():
    cowin = CoWinAPI()
    availability = cowin.get_availability_by_district("395", date="03-05-2021", fees=Fees.PAID)

    assert isinstance(availability, dict)
    assert isinstance(availability.get('centers'), list)
