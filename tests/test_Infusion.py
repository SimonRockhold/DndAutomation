from Character import Character
from Infusion import ArmorInfusion, WeaponInfusion, ItemInfusion
from Equipment import Armor, InventoryItem, Weapon
from PlayerClass import Artificer, PlayerClass
import unittest

class test(unittest.TestCase):
    def setUp(self) -> None:
        self.artificer = Artificer(levels=5)
        scaleMail = Armor('Scale Mail', 'it\'s some pretty neat armor', 14, 'medium')
        self.inventory = dict()
        weapons = dict()
        self.inventory['weapons'] = weapons
        self.inventory[scaleMail.name] = scaleMail
        self.enhancedDefence = ArmorInfusion('Enhanced Defence', 'plus 1', scaleMail)

        # initialize weapons
        # Warhammer
        warhammer = Weapon('Warhammer', 10, 'str', 'bludgeoning', 'versatile d8|d10, pretty cool hammer', {'martial weapons'})
        self.inventory[warhammer.name] = warhammer
        self.enhancedWeapon = WeaponInfusion('Enhanced Weapon', 'plus 1', warhammer)

        # Rifle
        rifle = Weapon('Rifle', 12, 'dex', 'piercing', 'range: 40|120, technically a musket, normally has the Reloading property', {'martial weapons', 'firearms'})
        self.inventory[rifle.name] = rifle
        self.repeatingShot = WeaponInfusion('Repeating Shot', 'Ignore repeating property, weapon plus 1', rifle)

        # Lance
        lance = Weapon('Lance', 12, 'str', 'piercing', 'reach, disadvantage within 5f', {'martial weapons'})
        self.inventory[lance.name] = lance
        self.armblade = WeaponInfusion('Armblade', 'this shouldn\'t actually exist in the inventory when not infused', lance)

        # Many handed pouch
        setOfPouches = InventoryItem('Set of pouches', 'a set of 5 pouches')
        self.manyHandedPouch = ItemInfusion('Many-Handed Pouch',
        'The infused pouches all share one interdimensional space of the same capacity as a single pouch. Thus, reaching into any of the pouches allows access to the same storage space. A pouch operates as long as it is within 100 miles of another one of the pouches; the pouch is otherwise empty and won\'t accept any contents. \n If this infusion ends, the items stored in the shared space move into one of the pouches, determined at random. The rest of the pouches become empty.',
        setOfPouches)
        self.inventory[setOfPouches.name] = setOfPouches
        

    def tearDown(self) -> None:
        del self.artificer, 
        self.enhancedDefence,
        self.repeatingShot,
        self.armblade,
        self.manyHandedPouch,
        self.inventory

    def test_Infusion(self):
        assert self.artificer.maxNumInfusionsPrepared == 2, 'max num infusions prepared should be half of max number of possible infusions'
        self.artificer.learnInfusions(self.enhancedWeapon, self.repeatingShot, self.armblade, self.manyHandedPouch)

        self.artificer.prepareInfusion(self.enhancedWeapon, self.inventory)
        self.artificer.prepareInfusion(self.repeatingShot, self.inventory)

        testitem = InventoryItem('test item', 'this is a test item')
        testitemInfusion = ItemInfusion('infused item', 'this is an infused item', testitem)
        with self.assertRaises(Exception):
            self.artificer.learnInfusions(testitemInfusion)
        with self.assertRaises(Exception):
            self.artificer.prepareInfusion(self.enhancedWeapon)
        print(self.artificer.knownInfusions)
        assert len(self.artificer.knownInfusions) == 2, 'infusions are moved to preparedInfusions'
        self.artificer.clearInfusions(self.inventory)
        assert len(self.artificer.knownInfusions) == 4, 'all infusions should be back in known infusions'
        return

if __name__ == '__main__':
    unittest.main()