# %%

from Spell import Spell
import json

class SpellLoader:
    def __init__(self, filename:str) -> None:
        self.fullFilePath = f"data/{filename}"
        with open(self.fullFilePath) as json_file:
            self.data = json.load(json_file)

        self.spells = self.createSpellDict(self.data)

    def createSpellDict(self, data):
        spells = dict()
        for json_spell in data:
            spell = self.interpretSpell_json(json_spell)
            spells[spell.name] = spell
        return spells

    def interpretSpell_json(self, spell_json: dict) -> Spell:
        appendix = {
            'A': 'Abjuration',
            'T': 'Transmutation',
            'C': 'Conjuration',
            'D': 'Divination',
            'E': 'Enhantment',
            'V': 'Evocation',
            'I': 'Illusion',
            'N': 'Necromancy',
            }

        name = spell_json['name']
        level = spell_json['level']
        school = appendix[spell_json['school']]
        time = spell_json['time'][0]
        range = spell_json['range']
        components = spell_json['components']
        duration = spell_json['duration'][0]
        concentration = 'concentration' in duration
        ritual = 'meta' in spell_json
        entries = spell_json['entries']

        return Spell(name, level, school, time, range, components, duration, entries, concentration, ritual) 

def default():
    with open('spells-sublist-data.json') as json_file:
        data = json.load(json_file)
    return data