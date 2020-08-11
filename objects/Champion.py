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
            champQ = Ability.Ability.fromJson(spells[0], Ability.AbilityKind.Q)
            champW = Ability.Ability.fromJson(spells[1], Ability.AbilityKind.W)
            champE = Ability.Ability.fromJson(spells[2], Ability.AbilityKind.E)
            champR = Ability.Ability.fromJson(spells[3], Ability.AbilityKind.R)
            champPassive = Ability.Ability.fromJson(champion['passive'], Ability.AbilityKind.PASSIVE)
            skills["PASSIVE"] = champPassive
            skills["Q"] = champQ
            skills["W"] = champW
            skills["E"] = champE
            skills["R"] = champR
        return skills

    def update(self):
        url = "https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion/{champion}.json".format(
            version="10.16.1",
            champion=self.name)
        with urllib.request.urlopen(url) as url:
            data = json.loads(url.read().decode())
            with open("testingDir/{champion}.json".format(champion=self.name), "w") as output:
                json.dump(data, output)