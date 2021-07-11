# %%
# test
from PlayerClass import Artificer
from Equipment import Weapon
from Infusion import WeaponInfusion
import unittest

import os

print(os.getcwd())


class test(unittest.TestCase):
    def setUp(self):
        self.c = Artificer(12, 16, 15, 20, 14, 11, proficiencyBonus=3, health=38)
        self.c.maxNumInfusions = 6
        warhammer = Weapon('Warhammer', 12, 'str', 'bludgeoning', 'this is a warhammer', requiredProficiency={'martial weapons'})
        self.c.addWeaponToInventory(warhammer)
        self.enhancedWeapon = WeaponInfusion('Enhanced Weapon', 'plus 1', warhammer)
        self.c.learnInfusion(self.enhancedWeapon)
        return

    def tearDown(self) -> None:
        del self.c
        del self.enhancedWeapon
        return

    def test_Weapon(self):
        assert self.c.attack('Warhammer') == (1, 1), 'when character is not proficient, atk = abilityMod, dmg = abilityMod'
        self.c.proficiencies = {'simple weapons', 'martial weapons'}
        assert self.c.attack('Warhammer') == (4, 1), 'when proficient, add profmod'
        self.c.prepareInfusion(self.enhancedWeapon)
        assert self.c.attack('Warhammer') == (9, 6), 'when infused, use intmod and add magicMod'
        return

if __name__ == '__main__':
    unittest.main()

# %%
