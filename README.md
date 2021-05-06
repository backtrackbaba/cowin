# Cowin Tracker

Python API wrapper for CoWin, India's digital platform launched by the government to help citizens register themselves
for the vaccination drive by booking an appointment at the nearby vaccination centres

The process to look-up for available slots to take the vaccine is tedious as you need to log in to the portal every time

This wrapper is meant to enable folks to build their own versions of a system to lookup for vaccine availablity either
in a district or in a particular pin code.

Example:

```python
from cowin_api import CoWinAPI

cowin = CoWinAPI()

states = cowin.get_states()
print(states)
```

# Install

`pip install cowin`

# Usage

The wrapper currently covers four endpoints used by the CoWin portal specified below.

## Initialize

```python
from cowin_api import CoWinAPI

cowin = CoWinAPI()
```

## Get all the available states

Returns the list of states in which vaccine drive is being conducted. This also returns the `state_id` which would be
required in the subsequent requests.

```python
from cowin_api import CoWinAPI

cowin = CoWinAPI()
states = cowin.get_states()
print(states)
```

<details>
  <summary>Sample Response:</summary>

```json
{
  "states": [
    {
      "state_id": 1,
      "state_name": "Andaman and Nicobar Islands"
    },
    {
      "state_id": 2,
      "state_name": "Andhra Pradesh"
    }
  ],
  "ttl": 24
}
```

</details>

---

## Get all the available districts

Returns the list of districts in a particular states in which vaccine drive is being conducted. This also returns
the `district_id` which would be required in the subsequent requests.

In this method, you would need to pass the `state_id` retrieved from the previous method.

```python
from cowin_api import CoWinAPI

state_id = '21'
cowin = CoWinAPI()
districts = cowin.get_districts(state_id)
print(districts)

```

<details>
  <summary>Sample Response:</summary>

```json
{
  "districts": [
    {
      "district_id": 395,
      "district_name": "Mumbai"
    },
    {
      "district_id": 363,
      "district_name": "Pune"
    }
  ],
  "ttl": 24
}
```

</details>

---

## Get all the centers available in a district

Use this method to lookup for centers based on a `district_id` or a list of `district_ids`. This method is broader than
searching by pin code as it covers the whole district.

In this method, you would need to pass the `district_id` retrieved from the previous methods. By default, the method
looks-up for slots with today's date. For any other dates pass the date in DD-MM-YYYY format.

```python
from cowin_api import CoWinAPI

district_id = '395'
date = '03-05-2021'  # Optional. Takes today's date by default
min_age_limit = 18  # Optional. By default returns centers without filtering by min_age_limit

cowin = CoWinAPI()
available_centers = cowin.get_availability_by_district(district_id, date, min_age_limit)
print(available_centers)
```

<details>
  <summary>Sample Response:</summary>

```json
{
  "centers": [
    {
      "center_id": 561660,
      "name": "BKC COVID Facility4 (18-44 Yr)",
      "state_name": "Maharashtra",
      "district_name": "Mumbai",
      "block_name": "Ward H East Corporation - MH",
      "pincode": 400051,
      "lat": 19,
      "long": 72,
      "from": "09:00:00",
      "to": "17:00:00",
      "fee_type": "Free",
      "sessions": [
        {
          "session_id": "524ee1c1-550f-4e02-be36-79259175aa30",
          "date": "02-05-2021",
          "available_capacity": 0,
          "min_age_limit": 18,
          "vaccine": "",
          "slots": [
            "09:00AM-11:00AM",
            "11:00AM-01:00PM",
            "01:00PM-03:00PM",
            "03:00PM-05:00PM"
          ]
        },
        {
          "session_id": "faf4a93e-fdf2-48f2-93de-254d19136d87",
          "date": "03-05-2021",
          "available_capacity": 0,
          "min_age_limit": 18,
          "vaccine": "",
          "slots": [
            "09:00AM-11:00AM",
            "11:00AM-01:00PM",
            "01:00PM-03:00PM",
            "03:00PM-05:00PM"
          ]
        }
      ]
    }
  ]
}
```

</details>


---

## Get all the available centers in a pin code

Use this method to lookup for centers based on a `pin_code` or a list of `pin_codes`. By default, the method looks-up
for slots with today's date. For any other dates pass the date in DD-MM-YYYY format.

```python
from cowin_api import CoWinAPI

pin_code = "400080"
date = '03-05-2021'  # Optional. Default value is today's date
min_age_limit = 18  # Optional. By default returns centers without filtering by min_age_limit

cowin = CoWinAPI()
available_centers = cowin.get_availability_by_pincode(pin_code, date, min_age_limit)
print(available_centers)
```

<details>
  <summary>Sample Response:</summary>

```json
{
  "centers": [
    {
      "center_id": 574933,
      "name": "SEVEN HIILS 2 Age (18-44)",
      "state_name": "Maharashtra",
      "district_name": "Mumbai",
      "block_name": "Ward K East Corporation - MH",
      "pincode": 400059,
      "lat": 19,
      "long": 72,
      "from": "09:00:00",
      "to": "17:00:00",
      "fee_type": "Free",
      "sessions": [
        {
          "session_id": "0645407e-fe72-4483-85d4-99ba4c567758",
          "date": "03-05-2021",
          "available_capacity": 0,
          "min_age_limit": 18,
          "vaccine": "",
          "slots": [
            "09:00AM-11:00AM",
            "11:00AM-01:00PM",
            "01:00PM-03:00PM",
            "03:00PM-05:00PM"
          ]
        },
        {
          "session_id": "0c4bc740-5429-4359-a2a4-428cf8649e38",
          "date": "08-05-2021",
          "available_capacity": 0,
          "min_age_limit": 45,
          "vaccine": "",
          "slots": [
            "09:00AM-11:00AM",
            "11:00AM-01:00PM",
            "01:00PM-03:00PM",
            "03:00PM-05:00PM"
          ]
        }
      ]
    },
    {
      "center_id": 574931,
      "name": "SEVEN HIILS 1",
      "state_name": "Maharashtra",
      "district_name": "Mumbai",
      "block_name": "Ward K East Corporation - MH",
      "pincode": 400059,
      "lat": 19,
      "long": 72,
      "from": "09:00:00",
      "to": "18:00:00",
      "fee_type": "Free",
      "sessions": [
        {
          "session_id": "819ca013-67f5-4074-8614-f49b7c41878f",
          "date": "08-05-2021",
          "available_capacity": 0,
          "min_age_limit": 45,
          "vaccine": "",
          "slots": [
            "09:00AM-11:00AM",
            "11:00AM-01:00PM",
            "01:00PM-03:00PM",
            "03:00PM-06:00PM"
          ]
        }
      ]
    },
    {
      "center_id": 574935,
      "name": "SEVEN HIILS 3",
      "state_name": "Maharashtra",
      "district_name": "Mumbai",
      "block_name": "Ward K East Corporation - MH",
      "pincode": 400059,
      "lat": 19,
      "long": 72,
      "from": "12:00:00",
      "to": "17:00:00",
      "fee_type": "Free",
      "sessions": [
        {
          "session_id": "4cfc728b-ce00-4e39-9285-8679130fbcb0",
          "date": "08-05-2021",
          "available_capacity": 0,
          "min_age_limit": 45,
          "vaccine": "",
          "slots": [
            "12:00PM-01:00PM",
            "01:00PM-02:00PM",
            "02:00PM-03:00PM",
            "03:00PM-05:00PM"
          ]
        }
      ]
    }
  ]
}
```

</details>

---

# Notes:

The API's of CoWin may at times return a 401 Unauthorized response. To mitigate this we are passing user agents in the
request. Still, if the issue persists please wait for a few minutes before trying again.

Please try not to spam the CoWin servers and try to keep a timeout between subsequent requests if you are polling at a
fixed interval

---

# Roadmap:

- [x] Add a filter to search by age group of 18-45 and 45+
- [x] Allow user to search for multiple pin codes
- [x] Allow user to search for multiple districts
- [ ] Catch and raise custom exceptions
- [ ] Implement Rate Limiting
- [ ] Implement mocking in test cases

---

# Contributions

Contributions are always welcome!

The roadmap given above is just a line of thought. Please feel free to contribute any other method which you feel could
be helpful.

---

# License:

MIT License
