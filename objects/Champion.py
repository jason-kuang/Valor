import urllib.request
import json
from objects import Ability


class Champion:
    def __init__(self, name):
        self.name = name

    def abilities(self) -> dict:
        skills = {}
        with open('champions/{champion}.json'.format(champion=self.name), encoding="utf8") as champData:
            champion = json.load(champData)['data'][self.name]
            spells = champion['spells']
            skills["PASSIVE"] = Ability.Ability.fromJson(champion['passive'], Ability.AbilityKind.PASSIVE)
            skills["Q"] = Ability.Ability.fromJson(spells[0], Ability.AbilityKind.Q)
            skills["W"] = Ability.Ability.fromJson(spells[1], Ability.AbilityKind.W)
            skills["E"] = Ability.Ability.fromJson(spells[2], Ability.AbilityKind.E)
            skills["R"] = Ability.Ability.fromJson(spells[3], Ability.AbilityKind.R)
        return skills

    def update(self):
        url = "https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion/{champion}.json".format(
            version="10.16.1",
            champion=self.name)
        with urllib.request.urlopen(url) as url:
            data = json.loads(url.read().decode())
            with open("champions/{champion}.json".format(champion=self.name), "w") as output:
                json.dump(data, output)