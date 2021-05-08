from datetime import datetime

from cowin_api.constants import Constants


def today() -> str:
    return datetime.now().strftime(Constants.DD_MM_YYYY)


def filter_centers(data: dict, filters: dict):
    filtered_centers = {'centers': []}
    centers = list(filter(lambda c: c['fee_type'] in filters.get('fee_type'), data.get('centers')))
    for center in centers:
        filtered_sessions = []
        for session in center.get('sessions'):
            if session.get('min_age_limit') == filters.get('min_age_limit') and session.get('vaccine') in filters.get(
                    'vaccine') and session.get('available_capacity') >= filters.get('available_capacity'):
                filtered_sessions.append(session)
        if len(filtered_sessions) > 0:
            center['sessions'] = filtered_sessions
            filtered_centers['centers'].append(center)

    return filtered_centers
