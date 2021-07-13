from math import inf
import Character
from Infusion import Infusion

class PlayerClass:
    '''Abstract base class that represents elements common to playerClasses'''
    def __init__(self) -> None:
        self.name = None
        self.character = None
        self.spellCastingAbility = None
        return

class Artificer(PlayerClass):
    # Infusions are unique to Artificers
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Artificer'
        self.spellcastingAbility = 'int'
        self.spellSaveDC = None
        self.spellAttackBonus = None
        
        # Infusions
        self.maxNumInfusions = None
        # self.maxNumInfusionsPrepared
        self.knownInfusions = set()
        self.preparedInfusions = set()

        self.characterInventory = None
    # END init

    @property
    def maxNumInfusionsPrepared(self):
        '''Getter for maxNumInfusions. No setter provided intentionally as value is always half of maxNumInfusions'''
        return self.maxNumInfusions // 2

    @property
    def totalNumInfusions(self):
        '''Return the number of infusions both prepared and known'''
        return len(self.knownInfusions) + len(self.preparedInfusions)

    def canLearnInfusion(self, infusion:Infusion) -> bool:

        if (infusion in self.knownInfusions) or (infusion in self.preparedInfusions):
            raise Exception(f"Infusion ({infusion.name}) already known")
        totalNumInfusions = len(self.knownInfusions) + len(self.preparedInfusions)
        if totalNumInfusions >= self.maxNumInfusions:
            raise Exception('Max number of infusions reached')
        return

    #def learnInfusion(self, *infusions):
    #    """Add Infusion to set of known Infusions"""
    #    newNumTotalInfusions = self.totalNumInfusions + len(infusions)
    #    if newNumTotalInfusions >= self.maxNumInfusions:
    #        raise Exception('New Infusions would exceed max number of Infusions')
    #    for i in infusions:
    #        if i in self.knownInfusions:
    #            raise Exception(f"Infusion ({i.name}) already known")
    #        # self.canLearnInfusion(i)
    #        self.knownInfusions.add(i)
    #    return

    def learnSingleInfusion(self, infusion_in):
        if not isinstance(infusion_in, Infusion):
            raise TypeError(f"{infusion_in} is not an Infusion")
        if (infusion_in in self.knownInfusions) or (infusion_in in self.preparedInfusions):
            raise Exception(f"Infusion ({infusion_in.name}) already known")
        self.knownInfusions.add(infusion_in)

        return

    def learnInfusions(self, *infusions):
        newNumTotalInfusions = self.totalNumInfusions + len(infusions)
        if newNumTotalInfusions >= self.maxNumInfusions:
            raise Exception('New Infusions would exceed max number of Infusions')

        for i in infusions:
            self.learnSingleInfusion(i)
        return

    # TODO allow multiple infusions to be passed as arguments to bulk-prepare Infusions
    def prepareInfusion(self, infusion: Infusion, characterInventory: dict):
        """Add infusion(s) to the set of prepared infusions
        
        Checks that number of prepared infusions is <= number of elements 
        in preparedInfusions
        """
        if infusion in self.preparedInfusions:
            raise Exception('Infusion already prepared')
        if infusion not in self.knownInfusions:
            raise Exception(f"Infusion({infusion.name}) not yet known")
        if len(self.preparedInfusions) >= self.maxNumInfusionsPrepared:
            raise Exception('cannot prepare more infusions')
        # Add the named Infusion to preparedInfusions and remove from knownInfusions
        self.preparedInfusions.add(infusion)
        self.knownInfusions.remove(infusion)
        infusion.activate(characterInventory)
        pass

    def clearInfusions(self):
        """Deactivate and unprepare all infusions"""
        i:Infusion
        for i in self.preparedInfusions:
            i.deactivate(self.inventory)
        self.knownInfusions.update(self.preparedInfusions)
        self.preparedInfusions.clear()

class BattleSmith(Artificer):
    def __init__(self, strength: int, dextertity: int, constitution: int, intelligence: int, wisdom: int, charisma: int, level: int, proficiencyBonus: int, health: int) -> None:
        super().__init__(strength, dextertity, constitution, intelligence, wisdom, charisma, level, proficiencyBonus, health)
        self.steelDefender = SteelDefender(self)
        return

class SteelDefender:
    def __init__(self, artificer: Artificer) -> None:
        self.artificer = artificer
        self.armorClass = 15
        self.maxHealth = 2 + self.artificer.character.abilityScores['int'][1] + (artificer.level * 5)
        self.abilityScores = {
        'str':(14, 2),
        'dex':(12, 1),
        'con':(14, 2),
        'int':(4, -3),
        'wis':(10, 0),
        'cha':(6, -2)}

        return 
    def attack_str(self):
        atk = self.artificer.spellAttackBonus
        dmg = self.artificer.profBonus
        return f"atk: 1d20 + {atk}, dmg: 1d8 + {dmg}"




# %%
