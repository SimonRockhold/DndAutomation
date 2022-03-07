import tkinter as tk
from tkinter import ttk

class Main_Window:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(self.parent)
        self.frame.grid(column=1, row=0, padx=5, pady=5)
        self.name_field = Name_field(self.frame)
        self.score_block = Ability_score_block(self.frame)
        player_classes = ('Artificer', 'Barbarian', 'Bard', 'Cleric', 'Druid', 'Fighter', 'Monk', 'Paladin', 'Ranger', 'Rogue', 'Sorcerer', 'Warlock', 'Wizard')
        self.class_selector = Class_selector(self.frame, player_classes)

        self.name_field.grid(padx=5, pady=5, sticky=tk.W)
        self.score_block.grid(padx=5, pady=5)
        self.class_selector.grid()

        ttk.Button(self.frame, text="print values", command=self.print_values).grid()

    def print_values(self):
        print(self.name_field.get_name())
        print(self.class_selector.get_selected())
        print(self.score_block.get_scores())

class Ability_score(ttk.Frame):
    def __init__(self, parent, name):
        super().__init__(parent)
        self.parent = parent
        self.name = name
        self.ability_score_val = tk.IntVar()
        abilityscore_validate_command = (self.parent.register(self.ability_validate),
            '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.label = tk.Label(self, text=self.name)
        ability_score_entry = tk.ttk.Entry(self, width=4, textvariable=self.ability_score_val, validate="key", validatecommand=abilityscore_validate_command)
        # ability_score_entry.grid(column=1, row=0, sticky=tk.E, padx=5)
        ability_score_entry.grid()


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

    def get_label(self):
        if self.label:
            return self.label
#END Ability_score

class Ability_score_block(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.str_box = Ability_score(self, name="Strength")
        self.dex_box = Ability_score(self, "Dexterity")
        self.con_box = Ability_score(self, "Constitution")
        self.int_box = Ability_score(self, "Intelligence")
        self.wis_box = Ability_score(self, "Wisdom")
        self.cha_box = Ability_score(self, "Charisma")

        tk.Label(self, text=self.str_box.name).grid(column=0, row=0)
        tk.Label(self, text=self.dex_box.name).grid(column=0, row=1)
        tk.Label(self, text=self.con_box.name).grid(column=0, row=2)
        tk.Label(self, text=self.int_box.name).grid(column=0, row=3)
        tk.Label(self, text=self.wis_box.name).grid(column=0, row=4)
        tk.Label(self, text=self.cha_box.name).grid(column=0, row=5)

        self.str_box.grid(column=1, row = 0)
        self.dex_box.grid(column=1, row = 1)
        self.con_box.grid(column=1, row = 2)
        self.int_box.grid(column=1, row = 3)
        self.wis_box.grid(column=1, row = 4)
        self.cha_box.grid(column=1, row = 5)
        
        # ttk.Button(self, text='print', command=self.get_scores).grid()

        
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


class Name_field(ttk.Frame):
    """Receive name entry"""
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.parent = parent
        
        name_validate_command = (self.parent.register(self.name_validate),
            '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        ttk.Label(self, text="character name").grid()
        self.name_var = tk.StringVar()
        # updates the value of data['name'] when the name entry is changed.
        #self.name_var.trace_add('write', update_name)
        name_entry = ttk.Entry(self, width=12, textvariable=self.name_var, validate="key", validatecommand=name_validate_command)
        name_entry.grid()
        

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

    def get_name(self):
        return self.name_var.get()
#END Name_field

class Class_selector(ttk.Frame):
    def __init__(self, parent, player_classes) -> None:
        super().__init__(parent)
        self.parent = parent
        self.player_classes = player_classes
        
        ttk.Label(self, text="Player Class").grid()
        # label_text = tk.StringVar()
        # update_label = ttk.Label(self.parent, textvariable=label_text).grid()
        self.class_var = tk.StringVar()
        player_class_selector = ttk.Combobox(self, textvariable=self.class_var)
        player_class_selector.bind('<<ComboboxSelected>>', lambda *defs : player_class_selector.selection_clear())
        player_class_selector['values'] = player_classes
        player_class_selector.grid()
        player_class_selector.state(['readonly'])

    def get_selected(self):
        return self.class_var.get()

    # def set_current_selection(selection):
    #     if selection in player_class_list:



#END Class_selector
    

def main(): 
    root = tk.Tk()
    app = Main_Window(root)
    root.mainloop()

if __name__ == '__main__':
    main()