from tkinter import *
from tkinter import ttk
import json

# this file should describe a window that guides the user through the bare minimum character definition:
# ie. character name, ability scores, race.
# should create a .json file with the name of the character as the name of the file.
# the file should contain either a short dict (in json form) or a Character object represented in json.

CHARACTER_FILEPATH = "data/characters/"

try:
    with open("data/player_classes.json") as json_file:
        player_classes = json.load(json_file)['player_classes']
except FileNotFoundError:
    print("data/player_classes.json not found, using defaults")
    player_classes = ('Artificer', 'Barbarian', 'Bard', 'Cleric', 'Druid', 'Fighter', 'Monk', 'Paladin', 'Ranger', 'Rogue', 'Sorcerer', 'Warlock', 'Wizard')

def create_file():
    # Save and quit.
    # sanitize name to be appropriate for a file name
    # remove leading whitespace before saving
    data['name'] = data['name'].lstrip()
    corrected_name = sanitize_filename(data['name'])

    data['ability_scores']['str'] = str_val.get()
    data['ability_scores']['dex'] = dex_val.get()
    data['ability_scores']['con'] = con_val.get()
    data['ability_scores']['int'] = int_val.get()
    data['ability_scores']['wis'] = wis_val.get()
    data['ability_scores']['cha'] = cha_val.get()

    #TODO check to see if there is a name collision and ask the user to confirm replacement
    with open(f"{CHARACTER_FILEPATH}{corrected_name}.json", 'w') as outfile:
        json.dump(data, outfile)
    
    print(data)
    root.destroy()

def sanitize_filename(character_name):
    #check if name is empty
    if not character_name:
        raise Exception("name must not be empty")
    #Remove preceding whitespace, replace whitespace with underscores, cast to lower case
    filename = character_name.lstrip().replace(" ", "_").lower()
    return filename

def update_name(*args):
    data['name'] = char_name.get()
    #print(data['name'])

data = {
    'name':"",
    'ability_scores':{
        'str':-1,
        'dex':-1,
        'con':-1,
        'int':-1,
        'wis':-1,
        'cha':-1
    },
    'race':""
}

# try:
#     with open(CHARACTER_FILEPATH) as json_file:
#         data = json.load(json_file)
# except FileNotFoundError:
#     with open(CHARACTER_FILEPATH, 'w') as outfile:
#         json.dump(data, outfile)

root = Tk()
root.title(CHARACTER_FILEPATH)

content_frame = ttk.Frame(root, padding="3 3 12 12")
content_frame.grid(column=0, row=0, sticky=(N, W, E, S))

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

###ENTRY BOX TEXT VALIDATION
#rules:
# [X] no leading whitespace
# [ ] no special characters
# [ ] no longer than [TODO determine max filename length, for now 10] characters
# %d = Type of action (1=insert, 0=delete, -1 for others)
# %i = index of char string to be inserted/deleted, or -1
# %P = value of the entry if the edit is allowed
# %s = value of entry prior to editing
# %S = the text string being inserted or deleted, if any
# %v = the type of validation that is currently set
# %V = the type of validation that triggered the callback
#      (key, focusin, focusout, forced)
# %W = the tk name of the widget

def name_validate(d, i, P, s, S, v, V, W):
    max_name_length = 32
    # Disallow leading whitespace
    if (not S == S.lstrip()) and int(i) < 1:
        root.bell()
        return False
    #prevent long names
    elif len(P) > max_name_length:
        return False
    else:
        return True

name_validate_command = (root.register(name_validate),
            #'%S')
            '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

#character name
character_name_row = 0
ttk.Label(content_frame, text="character name").grid(column=0, row=character_name_row)
char_name = StringVar()
# updates the value of data['name'] when the name entry is changed.
char_name.trace_add('write', update_name)
name_entry = ttk.Entry(content_frame, width=12, textvariable=char_name, validate="key", validatecommand=name_validate_command)
name_entry.grid(column=1, row=character_name_row)

#ABILITY SCORE ENTRIES
ttk.Label(content_frame, text="Define character values").grid(column=0, row=1)

def ability_validate(d, i, P, s, S, v, V, W):
    # ability scores should never be larger than 30
    # Disallow any non-number characters. 
    # TODO consider rather than disallow inputting value larger than 30,
    #   show error message and change text color to red.   
    print(S)
    if S.isnumeric() and not (len(P) > 0 and int(P) > 30):
        # int() will throw error when given and empty string, checks len first.
        return TRUE
    else:
        root.bell()
        # ding
        return FALSE

abilityscore_validate_command = (root.register(ability_validate),
            #'%S')
            '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

abilities_frame = ttk.Frame(content_frame, padding="3 3 12 12")
abilities_frame.grid(column=1, row=1, sticky=(N, W, E, S))

ability_score_row = 0
#STRENGTH
ttk.Label(abilities_frame, text="Strength").grid(column=0, row=ability_score_row)
str_val = IntVar()
str_entry = ttk.Entry(abilities_frame, width=4, textvariable=str_val, validate="key", validatecommand=abilityscore_validate_command)
str_entry.grid(column=2, row=ability_score_row)
ability_score_row += 1 #ensure that ability scores don't share the same row accidentally.
#DEXTERITY
ttk.Label(abilities_frame, text="Dexterity").grid(column=0, row=ability_score_row)
dex_val = IntVar()
dex_entry = ttk.Entry(abilities_frame, width=4, textvariable=dex_val, validate="key", validatecommand=abilityscore_validate_command)
dex_entry.grid(column=2, row=ability_score_row)
ability_score_row += 1
#CONSTITUTION
ttk.Label(abilities_frame, text="Constitution").grid(column=0, row=ability_score_row)
con_val = IntVar()
con_entry = ttk.Entry(abilities_frame, width=4, textvariable=con_val, validate="key", validatecommand=abilityscore_validate_command)
con_entry.grid(column=2, row=ability_score_row)
ability_score_row += 1
#INTELLIGENCE
ttk.Label(abilities_frame, text="Intelligence").grid(column=0, row=ability_score_row)
int_val = IntVar()
int_entry = ttk.Entry(abilities_frame, width=4, textvariable=int_val, validate="key", validatecommand=abilityscore_validate_command)
int_entry.grid(column=2, row=ability_score_row)
ability_score_row += 1
#WISDOM
ttk.Label(abilities_frame, text="Wisdom").grid(column=0, row=ability_score_row)
wis_val = IntVar()
wis_entry = ttk.Entry(abilities_frame, width=4, textvariable=wis_val, validate="key", validatecommand=abilityscore_validate_command)
wis_entry.grid(column=2, row=ability_score_row)
ability_score_row += 1
#CHARISMA
ttk.Label(abilities_frame, text="Charisma").grid(column=0, row=ability_score_row)
cha_val = IntVar()
cha_entry = ttk.Entry(abilities_frame, width=4, textvariable=cha_val, validate="key", validatecommand=abilityscore_validate_command)
cha_entry.grid(column=2, row=ability_score_row)
ability_score_row += 1

def update_player_class(*defs):
    data['player_class'] = class_var.get()
    player_class_selector.selection_clear()

#CLASS SELECTOR
player_class_row = ability_score_row + 1
ttk.Label(content_frame, text="Player Class").grid(column=0, row=player_class_row)
class_var = StringVar()
player_class_selector = ttk.Combobox(content_frame, textvariable=class_var)
player_class_selector.bind('<<ComboboxSelected>>', update_player_class)
player_class_selector['values'] = player_classes
player_class_selector.grid(column=1, row=player_class_row)
player_class_selector.state(['readonly'])

ttk.Button(content_frame, text="save and close", command=create_file).grid(column=0, row = player_class_row+1)


#add consistent padding to all elements in content_frame
for child in content_frame.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

root.mainloop()