from cowin_api.base_api import BaseApi
from cowin_api.constants import Constants
from cowin_api.utils import today


class CoWinAPI(BaseApi):

    def get_states(self):
        url = Constants.states_list_url
        return self._call_api(url)

    def get_districts(self, state_id: str):
        url = f"{Constants.districts_list_url}/{state_id}"
        return self._call_api(url)

    def get_availability_by_district(self, district_id: str, date: str = today()):
        url = f"{Constants.availability_by_district_url}?district_id={district_id}&date={date}"
        return self._call_api(url)

    def get_availability_by_pincode(self, pin_code: str, date: str = today()):
        url = f"{Constants.availability_by_pin_code_url}?pincode={pin_code}&date={date}"
        return self._call_api(url)
