# %%
from Equipment import Weapon
from PlayerClass import Artificer
from Infusion import *
from Spell import Spell
from SpellLoader import SpellLoader
  
bojon = Artificer(12, 16, 15, 20, 14, 11, level=6, proficiencyBonus=3, health=38)
bojon.addProficiencies('martial weapons', 'firearms')
bojon.maxNumInfusions = 6

# %% initialize weapons
# Warhammer
warhammer = Weapon('Warhammer', 10, 'str', 'bludgeoning', 'versatile d8|d10, pretty cool hammer', {'martial weapons'})
bojon.addWeaponToInventory(warhammer)
enhancedWeapon = WeaponInfusion('Enhanced Weapon', 'plus 1', warhammer)

# Rifle
rifle = Weapon('Rifle', 12, 'dex', 'piercing', 'range: 40|120, technically a musket, normally has the Reloading property', {'martial weapons', 'firearms'})
bojon.addWeaponToInventory(rifle)
repeatingShot = WeaponInfusion('Repeating Shot', 'Ignore repeating property, weapon plus 1', rifle)

# Lance
lance = Weapon('Lance', 12, 'str', 'piercing', 'reach, disadvantage within 5f', {'martial weapons'})
bojon.addWeaponToInventory(lance)
armblade = WeaponInfusion('Armblade', 'this shouldn\'t actually exist in the inventory when not infused', lance)

# Scale Mail
scaleMail = Armor('Scale Mail', 'it\'s some pretty neat armor', 14, 'medium')
bojon.addToInventory(scaleMail)
enhancedDefence = ArmorInfusion('Enhanced Defence', 'plus 1', scaleMail)
bojon.learnInfusion(enhancedDefence)

# Many-Handed Pouch
setOfPouches = InventoryItem('Set of pouches', 'a set of 5 pouches')
manyHandedPouch = ItemInfusion('Many-Handed Pouch',
    'The infused pouches all share one interdimensional space of the same capacity as a single pouch. Thus, reaching into any of the pouches allows access to the same storage space. A pouch operates as long as it is within 100 miles of another one of the pouches; the pouch is otherwise empty and won\'t accept any contents. \n If this infusion ends, the items stored in the shared space move into one of the pouches, determined at random. The rest of the pouches become empty.', setOfPouches)
bojon.learnInfusion(manyHandedPouch)
bojon.prepareInfusion(manyHandedPouch)

# Initialize Spell list
spellLoader = SpellLoader('Bojon_spell_list.json')
bojon.spells

# %%
