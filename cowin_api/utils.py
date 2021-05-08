from typing import Union, List

from datetime import datetime

from cowin_api.constants import Constants


def today() -> str:
    return datetime.now().strftime(Constants.DD_MM_YYYY)


def filter_centers(centers: dict, filter_col: List[str],
                   filter_val: List[Union[str, int]]):
    """A common function to apply filter at the second level of looping
    in the results returned by the api, we will do an assertion test of the
    data type for compatibility between filter col and filter val"""

    # any filter cols with None values should be ignored
    # first get the indices with non none values
    non_none_indices = set([index for index, val in enumerate(filter_val)\
                        if val is not None])
    # filter out the cols
    filter_col = [val for index, val in enumerate(filter_col)\
                   if index in non_none_indices]
    # filter out the values
    filter_val = [val for index, val in enumerate(filter_val)\
                   if index in non_none_indices]

    # if no filters, return as is
    if len(filter_col) == 0:
        return centers

    # first checks if the filter val are compatible with filter cols
    for index, col in enumerate(filter_col):
        assert isinstance(filter_val[index], Constants.col_to_data_type[col]),\
        f"[DATA TYPE INCOMPATIBLE] for filter {col}, expected instance of \
        {Constants.col_to_data_type[col]}, got {type(filter_val[index])}"

    original_centers = centers.get('centers')
    # this stores the results to be returned
    filtered_centers = {'centers': []}
    # level 1 loop
    for center in original_centers:
        filtered_sessions = []

        # iterate over the columns for any level 1 filter, if the filter
        # is passed, only then continue with the below
        keep_this_center = True
        for index, col in enumerate(filter_col):
            if Constants.col_to_loop_level[col] == 1:
                if isinstance(filter_val[index], str):
                    # make the check case insensitive
                    if not Constants.col_to_comparison[col](center.get(col).upper(),
                                                            filter_val[index].upper()):
                        # go to the next center
                        keep_this_center = False
                        break
                else:
                    # normal comparison
                    if not Constants.col_to_comparison[col](center.get(col),
                                                            filter_val[index]):
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
            for index, col in enumerate(filter_col):
                if Constants.col_to_loop_level[col] == 2:
                    if isinstance(filter_val[index], str):
                        # make the check case insensitive
                        if not Constants.col_to_comparison[col](session.get(col).upper(),
                                                                filter_val[index].upper()):
                            keep_this_session = False
                            break
                    else:
                        # normal comparison
                        if not Constants.col_to_comparison[col](session.get(col),
                                                                filter_val[index]):
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
