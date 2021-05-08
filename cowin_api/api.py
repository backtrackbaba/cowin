from typing import Union, List

from cowin_api.base_api import BaseApi
from cowin_api.constants import Constants
from cowin_api.utils import today, filter_centers


class CoWinAPI(BaseApi):

    def get_states(self):
        url = Constants.states_list_url
        return self._call_api(url)

    def get_districts(self, state_id: str):
        url = f"{Constants.districts_list_url}/{state_id}"
        return self._call_api(url)

    def get_availability_by_base(self, caller: str,
                                 areas: Union[str, List[str]],
                                 date: str, min_age_limit: int,
                                 min_capacity: int,
                                 vaccine: str,
                                 fee_type: str):
        """this function is called by the get availability function
        this is separated out so that the parent functions have the same
        structure and development becomes easier"""
        area_type, base_url = 'pincode', Constants.availability_by_pin_code_url
        if caller == 'district':
            area_type, base_url = 'district_id', Constants.availability_by_district_url
        # if the areas is a str, convert to list
        if isinstance(areas, str):
            areas = [areas]

        # make a separate call for each of the areas, first get all the
        # results and then apply the filters
        results = []
        for area_id in areas:
            url = f"{base_url}?{area_type}={area_id}&date={date}"
            curr_result = self._call_api(url)
            # append
            if curr_result:
                results += curr_result.get('centers')

        results = {'centers': results}

        # apply the filters
        # the change from min_capacity to available_capacity is requried
        # to keep consistency with columns names of results from api
        results = filter_centers(results,
                                 ['min_age_limit', 'available_capacity',
                                  'vaccine', 'fee_type'],
                                 [min_age_limit, min_capacity,
                                  vaccine, fee_type])

        # return the results in the same format as returned by the api
        return results

    def get_availability_by_district(self, district_id: Union[str, List[str]],
                                     date: str = today(),
                                     min_age_limit: int = None,
                                     min_capacity: int = None,
                                     vaccine: str = None,
                                     fee_type: str = None):
        return self.get_availability_by_base(caller='district', areas=district_id,
                                             date=date, min_age_limit=min_age_limit,
                                             min_capacity=min_capacity,
                                             vaccine=vaccine,
                                             fee_type=fee_type)

    def get_availability_by_pincode(self, pin_code: Union[str, List[str]],
                                    date: str = today(),
                                    min_age_limit: int = None,
                                     min_capacity: int = None,
                                     vaccine: str = None,
                                     fee_type: str = None):
        return self.get_availability_by_base(caller='pincode', areas=pin_code,
                                             date=date, min_age_limit=min_age_limit,
                                             min_capacity=min_capacity,
                                             vaccine=vaccine,
                                             fee_type=fee_type)
