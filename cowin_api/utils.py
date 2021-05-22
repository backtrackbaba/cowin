from datetime import datetime
from typing import Optional

from cowin_api.constants import Constants, Vaccine, Dose, Fees


def today() -> str:
    return datetime.now().strftime(Constants.DD_MM_YYYY)


def filter_centers(centers: dict, min_age_limit: Optional[int] = None, vaccine: Optional[Vaccine] = None,
                   dose: Optional[Dose] = None, fees: Optional[Fees] = None):
    original_centers = centers.get('centers')
    filtered_centers = {'centers': []}

    for index, center in enumerate(original_centers):
        if fees and not center.get('fee_type') == fees.value:
            continue

        filtered_sessions = []
        for session in center.get('sessions'):

            if min_age_limit and not session.get('min_age_limit') == min_age_limit:
                continue
            if vaccine and not session.get('vaccine') == vaccine.value:
                continue
            if dose and not session.get(dose.value) > 0:
                continue

            filtered_sessions.append(session)

        if filtered_sessions:
            center['sessions'] = filtered_sessions
            filtered_centers['centers'].append(center)

    return filtered_centers
