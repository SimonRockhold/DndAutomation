from functools import total_ordering
from typing import Dict

@total_ordering    
class Spell:
    def __init__(self, 
            name:str, 
            level: int, 
            school: str, 
            time: dict, 
            range: dict, 
            components: dict, 
            duration: dict,
            entries:list,
            concentration: bool = False,
            ritual: bool = False):
        self.name = name
        self.level = level
        self.school = school
        self.time = time
        self.range = range
        self.components = components
        self.duration = duration
        self.ritual = ritual
        self.concentration = concentration
        self.entries = entries

    def description_str(self):
        appendix = {
            'feet': 'ft',
            0:'Cantrip',
            1:'1st level',
            2:'2nd level',
            3:'3rd level',
            4:'4th level',
            5:'5th level',
            6:'6th level',
            7:'7th level',
            8:'8th level',
            9:'9th level'}
        description = f"""
{self.name} | {appendix[self.level]} | {self.school}
Casting time: {self.time_str()}
Range: {self.range_str()}
Components: {self.components_str()}
Duration: {self.duration_str()}
{self.entries_str()}

            """
        return description

        
    def range_str(self) -> str:
        r = self.range
        range = r['distance']['type']
        if 'amount' in r['distance']:
            amount = r['distance']['amount']
            unit = r['distance']['type']
            if r['type'] == 'radius':
                range = f"{amount} {unit} radius"
            else:
                range = f"{amount} {unit}"
        return range
    """
    possible range, 'type': point, cube, sphere, line, radius, cone
    range, distance, 'type': unlimited, sight, (miles, feet):amount
    """



    def time_str(self) -> str:
        '''human readable representation of spell casting time'''
        output = f"{self.time['number']} {self.time['unit']}"
        if 'condition' in self.time:
            output += ', which you take ' + self.time['condition']
        if self.concentration:
            output += ' (concentration)'
        return output

    def duration_str(self) -> str:
        output = ''
        durationType = self.duration['type']
        if durationType == 'timed':
            durationUnit = self.duration['duration']['type']
            durationNumber = self.duration['duration']['amount']
            if durationNumber > 1:
                durationUnit += 's'
            output += f"{durationNumber} {durationUnit}"
        if durationType == 'instant':
            output = 'instant'
        if durationType == 'permanent':
            output = 'permanent. '
            if 'ends' in self.duration:
                endCondition = self.duration['ends']
                output += 'end condition: '
                output += ', '.join(endCondition)
        return output
        

    def components_str(self) -> str:
        components = self.components
        verbal, somatic, material = False, False, None
        if 'v' in components:
            verbal = components['v']
        if 's' in components:
            somatic = components['s']
        if 'm' in components:
            if 'text' in components['m']:
                material = components['m']['text']
            else:
                material = components['m']
        output = []
        if verbal:
            output.append('V')
        if somatic:
            output.append('S')
        if material != None:
            output.append(f"M: {material}")
        return ', '.join(output)

    #def entries_str(self) -> str:
    #    output = list()
    #    output.append(self.entries[0])
    #    if len(self.entries) > 1:
    #        subEntries = self.entries[1:]
    #        print(subEntries[0])
    #        if subEntries[0]['type'] == 'entries':
    #            for i in subEntries:
    #                output.append(i['name'])
    #                output.append(i['entries'][0])
    #            
    #    return '\n    '.join(i for i in output)


    def entries_str(self) -> str:
        return self.entries

# is_valid_operand and __lt__ defined here to ensure that spells are sorted by level and then name
    def _is_valid_operand(self, other):
        return (hasattr(other, "name") and
                hasattr(other, "level"))

    def __lt__(self, other):
        '''\'less than\' behavior'''
        if not self._is_valid_operand(other):
            return NotImplemented
        return ((self.level, self.name.lower()) <
                (other.level, other.name.lower()))

    def __str__(self) -> str:
        return self.description_str()

    def __repr__(self) -> str:
        return f"Spell object: {self.name}, {self.level}, {self.school}, {self.range}, ritual={self.ritual}"
