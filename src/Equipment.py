class InventoryItem:
    """Describe an item that could be stored in the character inventory"""
    def __init__(self, name:str, description:str) -> None:
        self.name = name
        self.description = description

class Weapon(InventoryItem):
    """Represents a weapon"""
    def __init__(self, name:str, die:int, ability:str, dmgType:str, description, requiredProficiency:set = {'simple weapons'}, magicMod=0, numDice = 1):
        super().__init__(name, description)

        self.requiredProficiency = set(requiredProficiency)
        self.numDice = numDice
        self.die = die
        self.damageType = dmgType
        self.ability = ability
        self.magicMod = magicMod

    def copy(self):
        """Return shallow copy of this Weapon"""
        return Weapon(self.name, self.die, self.ability, self.damageType, self.description, self.requiredProficiency, self.magicMod, self.numDice)

    def __str__(self):
        """Return string representation of this Weapon instance"""
        return "{0}, d{1} {2} damage, {3}".format(self.name, self.die, self.damageType, self.description)
# End Weapon(InventoryItem)

class Armor(InventoryItem):
    """Represents Armor to be worn by a character"""
    def __init__(self, name:str, description:str, baseArmorClass:int, armorType:str, magicMod: int = 0) -> None:
        super().__init__(name, description)
        if armorType not in {'light', 'medium', 'heavy'}:
            raise Exception('Invalid armor type')

        self.magicMod = magicMod
        self.baseArmorClass = baseArmorClass
        self.armorType = armorType

    def armorClassValue(self, dexMod):
        """Calculate AC given armor type and Character dex, return AC""" 
        self.dexMod = dexMod
        armorClass = self.baseArmorClass
        if self.armorType   == 'light':
            armorClass += self.dexMod
        elif self.armorType == 'medium':
            armorClass += min(self.dexMod, 2)
        else:
            # Heavy armor case
            armorClass = self.baseArmorClass
        return armorClass + self.magicMod

    def copy(self):
        return Armor(self.name, self.description, self.baseArmorClass, self.armorType, self.magicMod)

# End Armor