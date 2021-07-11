from Equipment import Armor, InventoryItem, Weapon

class Infusion:
    def __init__(self, name:str, description:str) -> None:
        self.name = name
        self.description = description
        # self.additionalRules = additionalRule

    def __str__(self) -> str:
        return self.name

    def activate(self, inventory:dict):
        raise Exception('method not implemented')
    
    def deactivate(self, inventory:dict):
        raise Exception('method not implemented')

    def __repr__(self) -> str:
        return self.name

# end Infusion

class WeaponInfusion(Infusion):
    def __init__(self, name: str, description: str, infusedWeapon:Weapon = None, additionalRule:str = '') -> None:
        super().__init__(name, description)

        self.weapon = infusedWeapon
       # self.additionalRules = additionalRule
        self.infusedWeapon = infusedWeapon.copy()
        self.infusedWeapon.name = f"{self.infusedWeapon.name}({self.name})"
        self.infusedWeapon.magicMod = 1
        self.infusedWeapon.ability = 'int'

    def activate(self, inventory: dict):
        inventory['weapons'][self.weapon.name] = self.infusedWeapon
        return

    def deactivate(self, inventory: dict):
        inventory['weapons'][self.weapon.name] = self.weapon
        return

    def __str__(self) -> str:
        return self.infusedWeapon.name

# end WeaponInfusion

class ArmorInfusion(Infusion):
    '''Infusion that effects a set of armor in a player inventory'''
    def __init__(self, name: str, description: str, infusedArmor: Armor) -> None:
        super().__init__(name, description)
        
        self.armor = infusedArmor
        self.infusedArmor = infusedArmor.copy()
        self.infusedArmor.magicMod = 1

    def activate(self, inventory: dict):
        inventory[self.armor.name] = self.infusedArmor
        return

    def deactivate(self, inventory: dict):
        inventory[self.armor.name] = self.armor
        return  

# end ArmorInfusion

class ItemInfusion(Infusion):
    '''Infusion that adds a magic item to a player inventory when activated
    
    Item is removed when deactivated, and stored in ItemInfusion object.
    '''  
    def __init__(self, name: str, description: str, item: InventoryItem) -> None:
        super().__init__(name, description)

        self.item = item

    def activate(self, inventory: dict):
            inventory[self.item.name] = self.item
            return

    def deactivate(self, inventory: dict):
        '''Remove item from player inventory'''
        self.item = inventory.pop(self.item.name)
        return


    