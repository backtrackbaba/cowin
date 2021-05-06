from typing import Union, List

from cowin_api.base_api import BaseApi
from cowin_api.constants import Constants
from cowin_api.utils import today, filter_centers_by_age_limit


class CoWinAPI(BaseApi):

    def get_states(self):
        url = Constants.states_list_url
        return self._call_api(url)

    def get_districts(self, state_id: str):
        url = f"{Constants.districts_list_url}/{state_id}"
        return self._call_api(url)

    def get_availability_by_base(self, caller: str,
                                 areas: Union[str, List[str]],
                                 date: str, min_age_limt: int):
        """this function is called by the get availability function
        this is separated out so that the parent functions have the same
        structure and development becomes easier"""
        area_type, base_url = 'pincode', Constants.availability_by_pin_code_url
        if caller == 'district':
            area_type, base_url = 'district_id', Constants.availability_by_district_url
        # if the areas is a str, convert to list
        if isinstance(areas, str):
            areas = [areas]
        # make a separate call for each of the areas
        results = []
        for area_id in areas:
            url = f"{base_url}?{area_type}={area_id}&date={date}"
            if min_age_limt:
                curr_result = filter_centers_by_age_limit(self._call_api(url),
                                                          min_age_limt)
            else:
                curr_result = self._call_api(url)
            # append
            if curr_result:
                results += curr_result['centers']

        # return the results in the same format as returned by the api
        return {'centers': results}

    def get_availability_by_district(self, district_id: Union[str, List[str]],
                                     date: str = today(),
                                     min_age_limt: int = None):
        return self.get_availability_by_base(caller='district', areas=district_id,
                                             date=date, min_age_limt=min_age_limt)

    def get_availability_by_pincode(self, pin_code: Union[str, List[str]],
                                    date: str = today(),
                                    min_age_limt: int = None):
        return self.get_availability_by_base(caller='pincode', areas=pin_code,
                                             date=date, min_age_limt=min_age_limt)
