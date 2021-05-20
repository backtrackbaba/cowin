from datetime import datetime

from cowin_api.constants import Constants, Vaccine, Dose


def today() -> str:
    return datetime.now().strftime(Constants.DD_MM_YYYY)


def filter_centers_by_age_limit(centers: dict, min_age_limit: int):
    original_centers = centers.get('centers')
    filtered_centers = {'centers': []}
    for index, center in enumerate(original_centers):
        filtered_sessions = []
        for session in center.get('sessions'):
            if session.get('min_age_limit') == min_age_limit:
                filtered_sessions.append(session)
        if len(filtered_sessions) > 0:
            center['sessions'] = filtered_sessions
            filtered_centers['centers'].append(center)

    return filtered_centers


def filter_centers_by_vaccine(centers: dict, vaccine: Vaccine):
    original_centers = centers.get('centers')
    filtered_centers = {'centers': []}
    for index, center in enumerate(original_centers):
        filtered_sessions = []
        for session in center.get('sessions'):
            if session.get('vaccine') == vaccine.value:
                filtered_sessions.append(session)
        if len(filtered_sessions) > 0:
            center['sessions'] = filtered_sessions
            filtered_centers['centers'].append(center)
    return filtered_centers


def filter_centers_by_dose(centers: dict, dose: Dose):
    original_centers = centers.get('centers')
    filtered_centers = {'centers': []}
    for index, center in enumerate(original_centers):
        filtered_sessions = []
        for session in center.get('sessions'):
            if session.get(dose.value) > 0:
                filtered_sessions.append(session)
        if len(filtered_sessions) > 0:
            center['sessions'] = filtered_sessions
            filtered_centers['centers'].append(center)
    return filtered_centers
