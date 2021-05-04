class Constants:
    base_url = "https://cdn-api.co-vin.in/api/v2"

    states_list_url = f"{base_url}/admin/location/states"
    districts_list_url = f"{base_url}/admin/location/districts"

    availability_by_pin_code_url = f"{base_url}/appointment/sessions/public/calendarByPin"
    availability_by_district_url = f"{base_url}/appointment/sessions/public/calendarByDistrict"

    DD_MM_YYYY = "%d-%m-%Y"
