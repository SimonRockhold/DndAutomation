from Infusion import ArmorInfusion, WeaponInfusion, ItemInfusion
from Equipment import Armor, InventoryItem, Weapon
from PlayerClass import Artificer
import unittest

class test(unittest.TestCase):
    def setUp(self) -> None:
        self.c = Artificer(12, 16, 15, 20, 14, 11, proficiencyBonus=3, health=38)
        self.c.maxNumInfusions = 4
        scaleMail = Armor('Scale Mail', 'it\'s some pretty neat armor', 14, 'medium')
        self.c.addToInventory(scaleMail)
        self.enhancedDefence = ArmorInfusion('Enhanced Defence', 'plus 1', scaleMail)

        # initialize weapons
        # Warhammer
        warhammer = Weapon('Warhammer', 10, 'str', 'bludgeoning', 'versatile d8|d10, pretty cool hammer', {'martial weapons'})
        self.c.addWeaponToInventory(warhammer)
        self.enhancedWeapon = WeaponInfusion('Enhanced Weapon', 'plus 1', warhammer)

        # Rifle
        rifle = Weapon('Rifle', 12, 'dex', 'piercing', 'range: 40|120, technically a musket, normally has the Reloading property', {'martial weapons', 'firearms'})
        self.c.addWeaponToInventory(rifle)
        self.repeatingShot = WeaponInfusion('Repeating Shot', 'Ignore repeating property, weapon plus 1', rifle)

        # Lance
        lance = Weapon('Lance', 12, 'str', 'piercing', 'reach, disadvantage within 5f', {'martial weapons'})
        self.c.addWeaponToInventory(lance)
        self.armblade = WeaponInfusion('Armblade', 'this shouldn\'t actually exist in the inventory when not infused', lance)

        # Many handed pouch
        setOfPouches = InventoryItem('Set of pouches', 'a set of 5 pouches')
        self.manyHandedPouch = ItemInfusion('Many-Handed Pouch',
        'The infused pouches all share one interdimensional space of the same capacity as a single pouch. Thus, reaching into any of the pouches allows access to the same storage space. A pouch operates as long as it is within 100 miles of another one of the pouches; the pouch is otherwise empty and won\'t accept any contents. \n If this infusion ends, the items stored in the shared space move into one of the pouches, determined at random. The rest of the pouches become empty.',
        setOfPouches)

        return

    def tearDown(self) -> None:
        del self.c, 
        self.enhancedDefence,
        self.repeatingShot,
        self.armblade,
        self.manyHandedPouch
        return

    def test_Infusion(self):
        assert self.c.maxNumInfusionsPrepared == 2, 'max num infusions prepared should be half of max number of possible infusions'
        self.c.learnInfusion(self.enhancedWeapon)
        self.c.learnInfusion(self.repeatingShot)
        self.c.learnInfusion(self.armblade)
        self.c.learnInfusion(self.manyHandedPouch)

        self.c.prepareInfusion(self.enhancedWeapon)
        self.c.prepareInfusion(self.repeatingShot)

        testitem = InventoryItem('test item', 'this is a test item')
        testitemInfusion = ItemInfusion('infused item', 'this is an infused item', testitem)
        with self.assertRaises(Exception):
            self.c.learnInfusion(testitemInfusion)
        with self.assertRaises(Exception):
            self.c.prepareInfusion(self.enhancedWeapon)
        print(self.c.knownInfusions)
        assert len(self.c.knownInfusions) == 2, 'infusions are moved to preparedInfusions'
        self.c.clearInfusions()
        assert len(self.c.knownInfusions) == 4, 'all infusions should be back in known infusions'
        return

if __name__ == '__main__':
    unittest.main()