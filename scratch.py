import cassiopeia as cass
from cassiopeia.core import *


cass.set_default_region("NA")
cass.set_riot_api_key("")


def print_leagues():
    challenger = cass.get_challenger_league(queue=cass.Queue.ranked_solo_fives)
    summoner = Summoner(name="Elemental Scythe", region="NA")
    entries = summoner.league_entries
    print(challenger.to_json())







if __name__ == "__main__":
    print_leagues()