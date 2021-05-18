from datetime import datetime

from cowin_api.constants import Constants


def today() -> str:
    return datetime.now().strftime(Constants.DD_MM_YYYY)


def filter_centers_by_age_limit(centers: dict, min_age_limit: int):
    original_centers = centers.get('centers')
    filtered_centers = {'centers': []}
    for center in original_centers:
        filtered_sessions = [
            session
            for session in center.get('sessions')
            if session.get('min_age_limit') == min_age_limit
        ]

        if filtered_sessions:
            center['sessions'] = filtered_sessions
            filtered_centers['centers'].append(center)

    return filtered_centers
