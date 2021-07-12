# %% Character 
from Equipment import InventoryItem, Weapon, Armor
from Infusion import Infusion
from SpellLoader import SpellLoader, Spell
from Heritage import Heritage
import PlayerClass
import math

'''
maybe I should have the PlayerClass be a member of the Character class
    Character  
        -Artifier(PlayerClass)
            -Infusion
            -SteelDefende
        -Heritage
        -Spell
        -Equipment
'''
class Character:
    '''Describes the state of a character'''
    def __init__(self, strength:int, dextertity:int, constitution:int, intelligence:int, wisdom:int, charisma:int, level: int, playerClass: PlayerClass, maxHealth:int = None, heritage:Heritage = None) -> None:
        self.profBonus = math.ceil(level/4) + 1

        self.heritage = heritage
        # class-specific abilities should be located in a player class object rather than as an inheritance relationship
        self.playerClass = playerClass
        self.playerClass.linkToCharacter(self)

        self.proficiencies = set()
        self.proficiencies.add('simple weapons')

        self.abilities = list()

        self.level = level

        self.health = maxHealth
        self.maxHealth = maxHealth

        # Stores and initialized character raw scores and modifiers
        self.abilityScores = {
            'str':(strength,     self._getMod(strength)),
            'dex':(dextertity,   self._getMod(dextertity)),
            'con':(constitution, self._getMod(constitution)),
            'int':(intelligence, self._getMod(intelligence)),
            'wis':(wisdom,       self._getMod(wisdom)),
            'cha':(charisma,     self._getMod(charisma))}

        # store the Weapons currently held by the character
        self.weapons = {}

        # initialize to unarmored armor class
        self.unarmoredAC = 10 + self.dexMod
        # self.armorClass = self.unarmoredAC

        # accessed only through don() and doff() methods
        self._equippedArmorName:str = None

        self.inventory = {
            'weapons':self.weapons
        }

        # spellcasting
        self.spellcastingAbility: str = None
        self.spellSaveDC: int = None
        self.spellAttackBonus: int = None
        self.spells: Spell = None

    # End init
    def addPlayerClass(self, playerClass:PlayerClass):
        self.playerClass = playerClass
        return

    @classmethod
    def buildCharFromScratch(abilityScores, race):
        """NOT YET IMPLEMENTED"""
        return NotImplemented

    @property
    def armorClass(self):
        if self._equippedArmorName == None:
            return self.unarmoredAC
        return self.inventory[self._equippedArmorName].armorClassValue(self.dexMod)

    @property
    def dexMod(self):
        return self.abilityScores['dex'][1]

    def don(self, armorName:str):
        '''Equip armor given'''
        if self._equippedArmorName != None:
            raise Exception('armor is already equipped')
        self.armorToEquip: Armor = self.inventory[armorName]
        self._equippedArmorName = self.armorToEquip.name
        return

    def doff(self):
        '''Unequip equipped armor'''
        # self.armorClass = self.unarmoredAC
        self._equippedArmorName = None
        return

    def addToInventory(self, item:InventoryItem):
        self.inventory[item.name] = item
        return

    def takeDamage(self, damage:int):
        """Subtract damage from health"""
        self.health -= damage
        # print('New health = ' + str(self.health))
        return self.health

    def heal(self, healing:int):
        '''Add healing to health'''
        self.health += healing
        self.health = min(self.health, self.maxHealth)
        return self.health

    def _fullHeal(self):
        """Restore health to full"""
        self.health = self.maxHealth
        return

    def attack(self, weaponName:str):
        """Return tuple containing atk and dmg modifiers
        
        Calculates attack and damage modifiers given the weapon passed.
        """
        weapon:Weapon = self.weapons[weaponName]
        requiredProficiencies = weapon.requiredProficiency
        abilityMod = self.abilityScores[weapon.ability][1]
        atk = abilityMod + weapon.magicMod
        if requiredProficiencies.issubset(self.proficiencies):
            atk += self.profBonus
        dmg = abilityMod + weapon.magicMod
        return atk, dmg

    def attack_str(self, weaponName:str):
        '''Return string representation of weapon attack and damage rolls'''
        weapon:Weapon = self.weapons[weaponName]
        atk, dmg = self.attack(weaponName)
        return f"atk: 1d20 + {atk}, dmg: {weapon.numDice}d{weapon.die} + {dmg}"

    def addWeaponToInventory(self, weapon:Weapon):
        """Add provided Weapon to weapons dict"""
        self.weapons[weapon.name] = weapon
        return True

    def addProficiencies(self, *proficiency:str):
        for i in proficiency:
            self.proficiencies.add(i)
        return True

    def _getMod(self, i:int):
        """Return ability modifier given raw ability score"""
        return (i - 10) // 2

    def loadSpellsfromFile(self, filename):
        loader = SpellLoader(filename)
        self.spells = loader.spells
        return
        
# END Character class

class PlayerClass:
    def __init__(self) -> None:
        self.name = None
        self.character = None
        return

    def linkToCharacter(self, character: Character):
        '''Assign passed Character object, called by Character object'''
        self.character = character

class Artificer(PlayerClass):
    from Infusion import Infusion
    def __init__(self, character: Character) -> None:
        super().__init__(character)
        self.name = 'Artificer'
        self.spellcastingAbility = 'int'
        self.spellSaveDC = 8 + character.profBonus + character.abilityScores[self.spellcastingAbility][1]
        self.spellAttackBonus = character.profBonus + character.abilityScores[self.spellcastingAbility][1]
        
        # Infusions
        self.maxNumInfusions = None
        self.maxNumInfusionsPrepared
        self.knownInfusions = set()
        self.preparedInfusions = set()


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
        if infusion in self.knownInfusions or infusion in self.preparedInfusions:
            raise Exception(f"Infusion ({infusion.name}) already known")
        totalNumInfusions = len(self.knownInfusions) + len(self.preparedInfusions)
        if totalNumInfusions >= self.maxNumInfusions:
            raise Exception('Max number of infusions reached')
        return

    def learnInfusion(self, *infusions:Infusion):
        """Add Infusion to set of known Infusions"""
        newNumTotalInfusions = self.totalNumInfusions + len(infusions)
        if newNumTotalInfusions >= self.maxNumInfusions:
            raise Exception('New Infusions would exceed max number of Infusions')
        for i in infusions:
            self.canLearnInfusion(i)
            self.knownInfusions.add(i)
        return

    # TODO allow multiple infusions to be passed as arguments to bulk-prepare Infusions
    def prepareInfusion(self, infusion: Infusion):
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
        infusion.activate(self.character.inventory)
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
