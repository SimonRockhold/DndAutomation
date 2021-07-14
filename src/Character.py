# %% Character 
from Equipment import InventoryItem, Weapon, Armor
from SpellLoader import SpellLoader, Spell
from Heritage import Heritage
from PlayerClass import PlayerClass
import math

class Character:
    '''Describes the state of a character'''
    def __init__(self, strength:int, dextertity:int, constitution:int, intelligence:int, wisdom:int, charisma:int, level: int, playerClass: PlayerClass, maxHealth:int = None, heritage:Heritage = None) -> None:
        self.profBonus = math.ceil(level/4) + 1
        
        self.heritage = heritage
        # class-specific abilities should be located in a player class object rather than as an inheritance relationship
        self.playerClass: PlayerClass = playerClass
        #self.playerClass.linkToCharacter(self)

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
        self.spells: Spell = None
        self.playerClass.classSpells

        self.spellSaveDC: int = None
        self.spellAttackBonus: int = None
        self.spellcastingAbility = self.playerClass.spellCastingAbility
        if self.spellcastingAbility != None:
            self.spellSaveDC = 8 + self.profBonus + self.abilityScores[self.spellcastingAbility][1]
            self.spellAttackBonus = self.profBonus + self.abilityScores[self.spellcastingAbility][1]

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