from Character import Character
from PlayerClass import PlayerClass, Artificer
from Equipment import Armor
from Infusion import ArmorInfusion
import unittest

class test(unittest.TestCase):
    def setUp(self):
        self.c = Character(12, 20, 15, 20, 14, 11, level=6, playerClass=Artificer(), maxHealth=38)
        self.c.addProficiencies('martial weapons', 'firearms')
        self.c.playerClass.maxNumInfusions = 6
        
    def tearDown(self):
        del self.c

    def test_light_armor(self):
        leatherArmor = Armor('Leather Armor', 'some simple light armor', 11, 'light')
        self.c.addToInventory(leatherArmor)
        self.c.don('Leather Armor')
        assert self.c.armorClass == 16, '10 + dexmod = 16'
        self.c.doff()

    def test_medium_armor(self):
        chainShirt = Armor('Chain Shirt', 'it\'s some pretty neat armor', 13, 'medium')
        self.c.addToInventory(chainShirt)
        self.c.don('Chain Shirt')
        assert self.c.armorClass == 15, '13 + dexMod(5) (max 2)'
        self.c.doff()
        self.c.abilityScores['dex'] = (12, 1) #dexMod of 1
        self.c.don('Chain Shirt')
        assert self.c.armorClass == 14, '13 + dexMod(1) (max 2)'
        self.c.doff()


    def test_heavy_armor(self):
        # TODO when implemented, test whether a character not proficient in heavy armor is correctly debuffed
        plateArmor = Armor('Plate Armor', 'heavy armor test', 18, 'heavy')
        self.c.addToInventory(plateArmor)
        self.c.don('Plate Armor')
        assert self.c.armorClass == 18, 'dex mod should not be applied to heavy armor'
        self.c.doff()

    def test_unarmoredAC(self):
        assert self.c.armorClass == 15, 'no armor donned, AC should equal 10 + dexBonus(5)'


    def test_armor_infusion(self):
        
        scaleMail = Armor('Scale Mail', 'decent medium armor', 14, 'medium')
        self.c.addToInventory(scaleMail)
        self.enhancedDefence = ArmorInfusion('Enhanced Defence', 'plus 1', scaleMail)
        self.c.playerClass.learnInfusions(self.enhancedDefence)
        self.c.don('Scale Mail')
        assert self.c.armorClass == 16, 'when unenhanced, armor should be 16(10 + min(dexMod, 3)'
        self.c.playerClass.prepareInfusion(self.enhancedDefence, self.c.inventory)
        assert self.c.armorClass == 17, 'when enhanced, armor should be AC(16) + 1'
        self.c.doff()
        assert self.c.armorClass == 15, 'when no armor equipped, AC should equal unarmoredAC'

if __name__ == '__main__':
    unittest.main()

# nosetests