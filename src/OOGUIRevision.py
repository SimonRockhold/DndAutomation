import tkinter as tk
from tkinter import ttk

class Main_Window:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(self.parent)
        self.frame.grid(column=1, row=0, padx=5, pady=5)
        Name_field(self.frame)
        Ability_score_block(self.frame)
        player_classes = ('Artificer', 'Barbarian', 'Bard', 'Cleric', 'Druid', 'Fighter', 'Monk', 'Paladin', 'Ranger', 'Rogue', 'Sorcerer', 'Warlock', 'Wizard')
        Class_selector(self.frame, player_classes)


class Ability_score:
    def __init__(self, parent, name) -> None:
        self.parent = parent
        self.name = name
        self.ability_score_val = tk.IntVar()
        abilityscore_validate_command = (self.parent.register(self.ability_validate),
            '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        tk.Label(self.parent, text=self.name).grid(column=0)
        ability_score_entry = tk.ttk.Entry(self.parent, width=4, textvariable=self.ability_score_val, validate="key", validatecommand=abilityscore_validate_command)
        ability_score_entry.grid(column=1)


    def ability_validate(self, d, i, P, s, S, v, V, W):
        # ability scores should never be larger than 30
        # Disallow any non-number characters. 
        # TODO consider rather than disallow inputting value larger than 30,
        #   show error message and change text color to red.   
        print(S)
        if S.isnumeric() and not (len(P) > 0 and int(P) > 30):
            # int() will throw error when given and empty string, checks len first.
            return True
        else:
            self.parent.bell()
            # system ding
            return False
#END Ability_score

class Ability_score_block:
    def __init__(self, parent) -> None:
        self.parent = parent
        self.frame = tk.Frame(self.parent)
        self.frame.grid()
        self.str_box = Ability_score(self.frame, "Strength")
        self.dex_box = Ability_score(self.frame, "Dexterity")
        self.con_box = Ability_score(self.frame, "Constitution")
        self.int_box = Ability_score(self.frame, "Intelligence")
        self.wis_box = Ability_score(self.frame, "Wisdom")
        self.cha_box = Ability_score(self.frame, "Charisma")
        #ttk.Button(self.frame, text='print', command=self.get_scores).grid()
        
    def get_scores(self):
        str = self.str_box.ability_score_val.get()
        dex = self.dex_box.ability_score_val.get()
        con = self.con_box.ability_score_val.get()
        int = self.int_box.ability_score_val.get()
        wis = self.wis_box.ability_score_val.get()
        cha = self.con_box.ability_score_val.get()

        scores = str, dex, con, int, wis, cha
        # print(scores)
        return scores
#END Ability_score_block


class Name_field:
    def __init__(self, parent) -> None:
        self.parent = parent
        
        name_validate_command = (self.parent.register(self.name_validate),
            '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        ttk.Label(self.parent, text="character name").grid()
        char_name = tk.StringVar()
        # updates the value of data['name'] when the name entry is changed.
        #char_name.trace_add('write', update_name)
        name_entry = ttk.Entry(self.parent, width=12, textvariable=char_name, validate="key", validatecommand=name_validate_command)
        name_entry.grid()
        

    # def update_name(*args):
    #     data['name'] = char_name.get()
    #     #print(data['name'])

    def sanitize_filename(character_name):
        #check if name is empty
        if not character_name:
            raise Exception("name must not be empty")
        #Remove preceding whitespace, replace whitespace with underscores, cast to lower case
        filename = character_name.lstrip().replace(" ", "_").lower()
        return filename

    def name_validate(self, d, i, P, s, S, v, V, W):
        max_name_length = 32
        # Disallow leading whitespace
        if (not S == S.lstrip()) and int(i) < 1:
            self.parent.bell()
            return False
        #prevent long names
        elif len(P) > max_name_length:
            return False
        else:
            return True
#END Name_field

class Class_selector:
    def __init__(self, parent, player_classes) -> None:
        self.parent = parent
        self.player_classes = player_classes
        
        ttk.Label(self.parent, text="Player Class").grid()
        # label_text = tk.StringVar()
        # update_label = ttk.Label(self.parent, textvariable=label_text).grid()
        class_var = tk.StringVar()
        player_class_selector = ttk.Combobox(self.parent, textvariable=class_var)
        # player_class_selector.bind('<<ComboboxSelected>>', self.update_player_class)
        player_class_selector.bind('<<ComboboxSelected>>', lambda *defs : player_class_selector.selection_clear())
        player_class_selector['values'] = player_classes
        player_class_selector.grid()
        player_class_selector.state(['readonly'])


    def update_player_class(selector, text):
        selector.selection_clear()
        text.set(selector.getvar())

    # def set_current_selection(selection):
    #     if selection in player_class_list:



#END Class_selector
    

def main(): 
    root = tk.Tk()
    app = Main_Window(root)
    root.mainloop()

if __name__ == '__main__':
    main()