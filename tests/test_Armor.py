from PlayerClass import Artificer
from Equipment import Armor
from Infusion import ArmorInfusion
import unittest

class test(unittest.TestCase):
    def setUp(self):
        self.c = Artificer(12, 16, 15, 20, 14, 11, proficiencyBonus=3, health=38)
        self.c.maxNumInfusions = 6
        scaleMail = Armor('Scale Mail', 'it\'s some pretty neat armor', 14, 'medium')
        self.c.addToInventory(scaleMail)
        self.enhancedDefence = ArmorInfusion('Enhanced Defence', 'plus 1', scaleMail)
        self.c.learnInfusion(self.enhancedDefence)
        
        return

    def tearDown(self):
        del self.c
        del self.enhancedDefence

    def test_armor(self):

        self.c.don('Scale Mail')
        assert self.c.armorClass == 16, 'when unenhanced, armor should be 16'
        self.c.prepareInfusion(self.enhancedDefence)
        assert self.c.armorClass == 17, 'when enhanced, armor should be 17'
        self.c.doff()
        assert self.c.armorClass == 13, 'when no armor equiped, AC should equal 13'
        print('All armor tests passed')
        return


if __name__ == '__main__':
    unittest.main()

# nosetests