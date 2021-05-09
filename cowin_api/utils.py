from typing import Union, List

from datetime import datetime

from cowin_api.constants import Constants


def today() -> str:
    return datetime.now().strftime(Constants.DD_MM_YYYY)


def filter_centers(centers: dict, filters: dict):
    """A common function to apply filter at the second level of looping
    in the results returned by the api, we will do an assertion test of the
    data type for compatibility between filter col and filter val"""

    # had to move these definitions here since the col_to_comparison
    # needs to be generated dependant on what arguments are passed in the filters
    """a dictionary to store which columns appear at which level in the
    returned results to help with the looping"""
    col_to_loop_level = {
        'min_age_limit': 2,
        'available_capacity': 2,
        'vaccine': 2,
        'fee_type': 1,
    }


    # any filter cols with None values should be ignored
    filters = {k:v for k, v in filters.items() if v is not None}

    # if no filters, return as is
    if not filters:
        return centers

    """a dictionary to store the comparison types of the various columns in
    the returned results x is from the data while y is the filter value
    passed to filter_centers"""
    col_to_comparison = {}
    # define the individual lambda functions for filters
    if 'min_age_limit' in filters:
        # convert to list
        if isinstance(filters.get('min_age_limit'), int):
            filters['min_age_limit'] = [filters.get('min_age_limit')]
        min_age_limit_filter = set(filters['min_age_limit'])
        col_to_comparison['min_age_limit'] = lambda x: x in min_age_limit_filter

    if 'available_capacity' in filters:
        col_to_comparison['available_capacity'] = lambda x: \
                                        x >= filters.get('available_capacity')

    if 'vaccine' in filters:
        # convert to list
        if isinstance(filters.get('vaccine'), str):
            filters['vaccine'] = [filters.get('vaccine')]
        vaccine_filter = set(map(str.upper, filters.get('vaccine')))
        col_to_comparison['vaccine'] = lambda x: x.upper() in vaccine_filter

    if 'fee_type' in filters:
        # convert to list
        if isinstance(filters.get('fee_type'), str):
            filters['fee_type'] = [filters.get('fee_type')]
        fee_filter = set(map(str.upper, filters.get('fee_type')))
        col_to_comparison['fee_type'] = lambda x: x.upper() in fee_filter

    # level 1 filter
    level_1_filter = lambda x: all([col_to_comparison.get(k)(x.get(k)) \
                               for k in filters if col_to_loop_level[k] == 1])
    # level 2 filter
    level_2_filter = lambda x: all([col_to_comparison.get(k)(x.get(k)) \
                               for k in filters if col_to_loop_level[k] == 2])

    # start the main filter processing
    original_centers = centers.get('centers')

    # apply level 1 filters
    filtered_centers = list(filter(level_1_filter, original_centers))

    if not filtered_centers:
        # return an empty list
        return {'centers': []}

    # apply level 2 filters
    print(filtered_centers)
    for center in filtered_centers:
        center['sessions'] = list(filter(level_2_filter, center.get('sessions')))

    # one more check is to remove those centers that do not have any
    filtered_centers = list(filter(lambda x: len(x.get('sessions')) > 0,
                                filtered_centers))

    if not filtered_centers:
        return {'centers': []}

    return {'centers': filtered_centers}
