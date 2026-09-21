import opendota
import asyncio
import logging
from dataclasses import dataclass
@dataclass
class DotaMatchData:
    match_id: int
    hero_id: int
    kills: int
    deaths: int
    assists: int
    purchase: list[str]
    last_hits: int
    denies: int
    win: int
    dewards: int
    rosh: int




api_logger = logging.getLogger("Client")


OPEN_DOTA = opendota.OpenDota()



def get_most_recent_match_id(steamID):
    print(f"DEBUG: awaiting getting player matches")
    match = OPEN_DOTA.get_player_matches(steamID)
    print(f"DEBUG: {match[0]['match_id']}")
    return match[0]['match_id']

async def request_match_parse(steamID):
    match_id = get_most_recent_match_id(steamID)

    result = OPEN_DOTA.request_parse(match_id)

    job_id = result['job']["jobId"]
    print(f'{job_id}')
    print(f"DEBUG: parse loop")
    while True:
        status = OPEN_DOTA.request_status(job_id)
        print(f"DEBUG: status = {status}")
        if status == None:
            break

        await asyncio.sleep(5)

    return OPEN_DOTA.get_match(match_id)

def get_my_player(players, steamID) -> dict:
    print(f"DEBUG: getting player")
    for player in players:
        if player['account_id'] == steamID:
            return player

    raise ValueError("Player not found in match")

async def parse_most_recent_match_data(steamID):
    print(f"DEBUG: Steam ID = {steamID}")
    match = await request_match_parse(steamID)
    match_id = match['match_id']
    print(f"{match_id}")
    players = match['players']
    my_player = get_my_player(players, steamID)
    api_logger.info(my_player["hero_id"])
    print(f"{my_player['hero_id']}")
    return DotaMatchData(
        match_id = match_id,
        hero_id = my_player['hero_id'],
        kills = my_player['kills'],
        deaths = my_player['deaths'],
        assists = my_player['assists'],
        purchase = list(my_player.get("purchase", {}).keys()),
        last_hits = my_player['last_hits'],
        denies = my_player['denies'],
        win = my_player['win'],
        dewards = my_player['observer_kills'] + my_player['sentry_kills'],
        rosh = my_player['roshan_kills']
    )



    

