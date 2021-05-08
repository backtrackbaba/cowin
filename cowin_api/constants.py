class Constants:
    base_url = "https://cdn-api.co-vin.in/api/v2"

    states_list_url = f"{base_url}/admin/location/states"
    districts_list_url = f"{base_url}/admin/location/districts"

    availability_by_pin_code_url = f"{base_url}/appointment/sessions/public/calendarByPin"
    availability_by_district_url = f"{base_url}/appointment/sessions/public/calendarByDistrict"

    DD_MM_YYYY = "%d-%m-%Y"

    """a dictionary to store which columns appear at which level in the
    returned results to help with the looping"""
    col_to_loop_level = {
        'min_age_limit': 2,
        'available_capacity': 2,
        'vaccine': 2,
        'fee_type': 1,
    }

    """a dictionary to store the data types of the various columns in
    the returned results to help with assertion checks"""
    col_to_data_type = {
        'min_age_limit': int,
        'available_capacity': int,
        'vaccine': str,
        'fee_type': str,
    }

    """a dictionary to store the comparison types of the various columns in
    the returned results x is from the data while y is the filter value
    passed to filter_centers"""
    col_to_comparison = {
        'min_age_limit': lambda x, y: True if x == y else False,
        'available_capacity': lambda x, y: True if x >= y else False,
        'vaccine': lambda x, y: True if x == y else False,
        'fee_type': lambda x, y: True if x == y else False,
    }
