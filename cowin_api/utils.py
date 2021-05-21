from datetime import datetime

from cowin_api.constants import Constants, Vaccine, Dose


def today() -> str:
    return datetime.now().strftime(Constants.DD_MM_YYYY)


def filter_centers(centers: dict, min_age_limit: int = None, vaccine: Vaccine = None, dose: Dose = None):
    original_centers = centers.get('centers')
    filtered_centers = {'centers': []}
    for index, center in enumerate(original_centers):
        filtered_sessions = []
        for session in center.get('sessions'):

            if min_age_limit and not session.get('min_age_limit') == min_age_limit:
                continue
            if vaccine and not session.get('vaccine') == vaccine.value:
                continue
            if dose and not session.get(dose.value) > 0:
                continue

            filtered_sessions.append(session)

        if len(filtered_sessions) > 0:
            center['sessions'] = filtered_sessions
            filtered_centers['centers'].append(center)

    return filtered_centers
