import json
import os
from dataclasses import dataclass

class HeritageLoader:
    def __init__(self, filename:str) -> None:
        self.filePath = os.getenv('DATADIR')
        self.fullFilePath = f"{self.filePath}/{filename}"
        with open(self.fullFilePath) as json_file:
            self.data = json.load(json_file)
        return

    def interpret_json(self):

        name: str = self.data['name']
        subrace: str = self.data['subrace']
        abilityScores = self.data['ability scores']
        speed: int = self.data['speed']
        size: int = self.data['size']
        languages: list = self.data['languages']

        abilities = self.abilityInterpreter(self.data['abilities'])
        
        misc = self.data['misc']
        return Heritage(name, subrace, abilityScores, speed, size, languages, abilities, misc)

    def abilityInterpreter(self, abilities: list):
        output = list()
        for a in abilities:
            output.append(Ability(a['name'], a['description']))
        return output

class Heritage:
    def __init__(self, name: str, subrace: str, abilityScores: dict, speed: int, size: int, languages: list, abilities: list, misc: list) -> None:
        self.name = name
        self.subrace = subrace
        self.abilityScores = abilityScores
        self.speed = speed
        self.size = size
        self.languages = languages
        self.abilities = abilities

    def __str__(self) -> str:
        return f"{self.name}({self.subrace})"

    def __repr__(self) -> str:
        return f"{self.name}({self.subrace}) size:{self.size} {self.abilities}"

@dataclass
class Ability:
    name: str
    description: str
    def __str__(self) -> str:
        return f"{self.name}\n{self.description}"

    def __repr__(self) -> str:
        return f"{self.name}, {self.description}"