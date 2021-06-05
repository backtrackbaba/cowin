class Constants:
    base_url = "https://cdn-api.co-vin.in/api/v2"

    states_list_url = f"{base_url}/admin/location/states"
    districts_list_url = f"{base_url}/admin/location/districts"

    availability_by_pin_code_url = f"{base_url}/appointment/sessions/public/calendarByPin"
    availability_by_district_url = f"{base_url}/appointment/sessions/public/calendarByDistrict"

    DD_MM_YYYY = "%d-%m-%Y"

    default_filters = {
        'min_age_limit': 18,
        'fee_type': ['Free', 'Paid'],
        'vaccine': ['COVISHIELD', 'COVAXIN', 'Sputnik V'],
        'available_capacity': 0,
        'available_capacity_dose1': 0,
        'available_capacity_dose2': 0
    }
