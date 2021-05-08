from typing import Union, List

from datetime import datetime

from cowin_api.constants import Constants


def today() -> str:
    return datetime.now().strftime(Constants.DD_MM_YYYY)


def filter_centers(centers: dict, filters: dict):
    """A common function to apply filter at the second level of looping
    in the results returned by the api, we will do an assertion test of the
    data type for compatibility between filter col and filter val"""

    # any filter cols with None values should be ignored
    filters = {k:v for k, v in filters.items() if v is not None}

    # if no filters, return as is
    if not filters:
        return centers

    # first checks if the filter val are compatible with filter cols
    for f_key in filters:
        assert isinstance(filters[f_key], Constants.col_to_data_type[f_key]),\
        f"[DATA TYPE INCOMPATIBLE] for filter {f_key}, expected instance of \
        {Constants.col_to_data_type[f_key]}, got {type(filters[f_key])}"

    original_centers = centers.get('centers')
    # this stores the results to be returned
    filtered_centers = {'centers': []}
    # level 1 loop
    for center in original_centers:
        filtered_sessions = []

        # iterate over the columns for any level 1 filter, if the filter
        # is passed, only then continue with the below
        keep_this_center = True
        for f_key in filters:
            if Constants.col_to_loop_level[f_key] == 1:
                if isinstance(filters[f_key], str):
                    # make the check case insensitive
                    if not Constants.col_to_comparison[f_key](center.get(f_key).upper(),
                                                              filters[f_key].upper()):
                        # go to the next center
                        keep_this_center = False
                        break
                else:
                    # normal comparison
                    if not Constants.col_to_comparison[f_key](center.get(f_key),
                                                              filters[f_key]):
                        # go to the next center
                        keep_this_center = False
                        break

        # go to the next center
        if not keep_this_center:
            continue

        # level 2 loop
        for session in center.get('sessions'):
            keep_this_session = True

            # iterate over the columns and check for filters
            for f_key in filters:
                if Constants.col_to_loop_level[f_key] == 2:
                    if isinstance(filters[f_key], str):
                        # make the check case insensitive
                        if not Constants.col_to_comparison[f_key](session.get(f_key).upper(),
                                                                  filters[f_key].upper()):
                            keep_this_session = False
                            break
                    else:
                        # normal comparison
                        if not Constants.col_to_comparison[f_key](session.get(f_key),
                                                                  filters[f_key]):
                            keep_this_session = False
                            break

            # go to the next session
            if not keep_this_session:
                continue

            # if we have reached this point, the session can be appended
            filtered_sessions.append(session)

        # checked if anything got filtered
        if len(filtered_sessions) > 0:
            center['sessions'] = filtered_sessions
            filtered_centers['centers'].append(center)

    return filtered_centers
