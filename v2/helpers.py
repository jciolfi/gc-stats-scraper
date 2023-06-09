from constants import *

# player names in GameChanger are listed as "First Last"
# this function converts names to the NCBA format, which is "Last, First"
def format_name(name: str):
    if ' ' not in name:
        return name
    split = name.index(' ')
    return f'{name[split+1:]}, {name[:split]}'


# build url for requesting stats given a team_id, query params, and filter dates
def build_stat_url(team_id, stat_params, start_ts, end_ts):
    url = f'{BASE_URL}{STATS_URI}{team_id}/{stat_params}'
    if start_ts:
        url += f'&start_ts={start_ts}'
    if end_ts:
        url += f'&end_ts={end_ts}'

    return url


# return 'players' array after requesting stats
def get_players_stats(session, url, session_cookies):
    payload = {}
    headers = { 'Cookie': session_cookies }
    response = session.request("GET", url, headers=headers, data=payload)
    return response.json()['players']


# print out dictionary in a prettier format
def print_dict(map):
    for key, val in map.items():
        print(f'{key}: {val}')
