# %%
# test
from Character import Character
from PlayerClass import Artificer, PlayerClass
from Equipment import Weapon
from Infusion import WeaponInfusion
import unittest

class test(unittest.TestCase):
    def setUp(self):
        self.character = Character(12, 16, 15, 20, 14, 11, level=6, playerClass = Artificer(levels=6), maxHealth=38)
        warhammer = Weapon('Warhammer', 12, 'str', 'bludgeoning', 'this is a warhammer', requiredProficiency={'martial weapons'})
        self.character.addWeaponToInventory(warhammer)
        self.enhancedWeapon = WeaponInfusion('Enhanced Weapon', 'plus 1', warhammer)
        self.character.playerClass.learnInfusions(self.enhancedWeapon)

    def tearDown(self) -> None:
        del self.character,
        self.enhancedWeapon

    def test_Weapon(self):
        assert self.character.attack('Warhammer') == (1, 1), 'when character is not proficient, atk = abilityMod, dmg = abilityMod'
        self.character.proficiencies = {'simple weapons', 'martial weapons'}
        assert self.character.attack('Warhammer') == (4, 1), 'when proficient, add profmod'
        self.character.playerClass.prepareInfusion(self.enhancedWeapon, self.character.inventory)
        assert self.character.attack('Warhammer') == (9, 6), 'when infused, use intmod and add magicMod'

if __name__ == '__main__':
    unittest.main()

# %%
