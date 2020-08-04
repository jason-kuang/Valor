import cassiopeia as cass
from cassiopeia.core import *
from cassiopeia import Summoner


cass.set_default_region("NA")
cass.set_riot_api_key("")


def print_leagues():
    challenger = cass.get_challenger_league(queue=cass.Queue.ranked_solo_fives)
    summoner = Summoner(name="Nightblue3", region="NA")
    entries = summoner.league_entries
    participant = summoner.current_match.participants
    for x in participant:
        print("{name} ({rank}) is playing {champion}".format(name = x.summoner.name, champion=x.champion.name, rank=x.summoner.level))







if __name__ == "__main__":
    print_leagues()