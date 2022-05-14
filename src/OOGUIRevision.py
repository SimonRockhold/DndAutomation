from cProfile import label
from sqlite3 import Row
import tkinter as tk
from tkinter import TclError, ttk
from turtle import bgcolor

from Character import Character

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Edit Character")

        model = Model()
        view = View(self)
        controller = Controller(model, view)

        view.set_controller(controller)


class View(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.controller = None
        self.window = Main_Window(parent=parent, view=self)

    def set_controller(self, controller):
        self.controller = controller

# End View

class Controller:
    def __init__(self, model, view) -> None:
        self.model = model
        self.view = view
        
    def save(self):
        return NotImplemented

    def print_values(self):
        temp = self.view.window
        print(temp.name_field.get_name())
        print(temp.class_selector.get_selected())
        print(temp.score_block.get_scores())
        
# End Controller

class Main_Window:
    # def __init__(self, parent, controller):
    def __init__(self, parent, view):

        self.view = view
        self.parent = parent
        self.frame = tk.Frame(self.parent)
        self.name_field = Name_field(self.frame)
        self.level_field = Level_field(self.frame)
        self.max_health = Health_field(self.frame)
        self.score_block = Ability_score_block(self.frame)
        player_classes = ('Artificer', 'Barbarian', 'Bard', 'Cleric', 'Druid', 'Fighter', 'Monk', 'Paladin', 'Ranger', 'Rogue', 'Sorcerer', 'Warlock', 'Wizard')
        self.class_selector = Class_selector(self.frame, player_classes)

        self.frame.grid(column=1, row=0, padx=5, pady=5)
        self.name_field.grid(padx=5, pady=5, sticky=tk.W)
        self.level_field.grid(column=1, row=0, padx=5, pady=5)
        self.max_health.grid(padx=5, pady=5, sticky=tk.W)
        self.score_block.grid(padx=5, pady=5)
        self.class_selector.grid()

        ttk.Button(self.frame, text="print values", command=self.button_pressed).grid()


    def button_pressed(self):
        if self.view.controller:
            self.view.controller.print_values()
        else:
            raise Exception

    def print_values(self):
        print(self.name_field.get_name())
        print(self.class_selector.get_selected())
        print(self.score_block.get_scores())


class Model:
    '''Model should not require knowledge of other components. Is responsible for storage and maybe data validation'''
    def __init__(self) -> None:
        self.character:Character = None
        self.data = {
            'name':None,
            'class':None,
            'level':None,
            'stats': {
                'str':None,
                'dex':None,
                'con':None,
                'int':None,
                'wis':None,
                'cha':None
                },
            'health':None,
            'race':None
        }

    def create_character(self, stat_array, level, player_class, max_health):
        self.character = Character(
            strength=stat_array['str'],
            dextertity=stat_array['dex'],
            constitution=stat_array['con'],
            intelligence=stat_array['int'],
            wisdom=stat_array['wis'],
            charisma=stat_array['cha'],
            playerClass=player_class, maxHealth=max_health,
            heritage=None
            )
        return NotImplemented
# End Model


class Ability_score(ttk.Frame):
    def __init__(self, parent, name):
        super().__init__(parent)
        self.parent = parent
        self.name = name
        self.ability_score_val = tk.IntVar()
        self.ability_score_val.set(10)
        self.ability_mod_val = tk.IntVar()
        abilityscore_validate_command = (self.parent.register(self.ability_validate),
            '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.label = tk.Label(self, text=self.name)
        self.ability_score_entry = tk.ttk.Entry(self, width=4, textvariable=self.ability_score_val, validate="key", validatecommand=abilityscore_validate_command)
        # self.ability_mod_label = tk.Label(self, textvariable=self.ability_mod_val)
        # ability_score_entry.grid(column=1, row=0, sticky=tk.E, padx=5)

        self.ability_score_entry.bind("<KeyRelease>", self.update_ability_mod)
        self.ability_score_entry.bind("<FocusOut>", self.set_empty_to_zero)

        self.ability_score_entry.grid()


    def ability_validate(self, action, index, value_if_allowed,
                       prior_value, text_delta, validation_type, trigger_type, widget_name):
        # -> ability scores should never be larger than 30 per the rulebook, but could occur in homebrew.
        # -> Disallow any non-number characters.    
        # allow empty value so that user can use backspace to get to the beginning before entering new value.     
        self.ability_score_entry.config({"foreground":"Black"})
        if not value_if_allowed:
            return True
        # otherwise only allow values that can be converted to an int
        if len(value_if_allowed)>1 and not value_if_allowed.lstrip('0') == value_if_allowed:
            self.ability_score_val.set(0)
            # return False
        try:
            value = int(value_if_allowed)
            # change text color to red if value is greater than 30
            if value > 30:
                self.ability_score_entry.config({"foreground":"Red"})
            else:
                self.ability_score_entry.config({"foreground":"Black"})
            return True
        except ValueError:
            return False

    def set_empty_to_zero(self, event):
        '''Called when focus is lost to replace empty cells with 0s'''
        if self.get_val() == -1:
            self.set_val(0)

    def update_ability_mod(self, event):
        # the get() method of the tk.IntVar will throw an error if the value is set to an empty string
        try:
            ability_score = self.ability_score_val.get()
            # print(f"({ability_score} - 10) / 2 = {(ability_score-10)//2}")
            self.ability_mod_val.set((ability_score - 10) // 2)
        except tk.TclError:
            # treat no value the same as 0 for simplicity's sake. (a score of 0 yields -5)
            self.ability_mod_val.set(-5)
            return

    def get_label(self):
        if self.label:
            return self.label

    def get_val(self):
        try:
            return self.ability_score_val.get()
        except tk.TclError:
            return -1

    def set_val(self, new_value):
        self.ability_score_val.set(new_value)

#END Ability_score

class Ability_score_block(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.ability_scores = [
            Ability_score(self, "Strength"),
            Ability_score(self, "Dexterity"),
            Ability_score(self, "Constitution"),
            Ability_score(self, "Intelligence"),
            Ability_score(self, "Wisdom"),
            Ability_score(self, "Charisma")
        ]

        row = 0
        for ability_score in self.ability_scores:
            tk.Label(self, text=ability_score.name).grid(column=0, padx=5, row=row, sticky=tk.NSEW)
            ability_score.grid(column=1, row=row, padx=5, sticky=tk.NSEW)
            tk.Label(self, textvariable=ability_score.ability_mod_val).grid(column=2, padx=10, row=row, sticky=tk.NSEW)
            # ability_score.ability_mod_label.grid(column=2, row=row, padx=5)
            row = row+1

        
    def get_scores(self):
        raw_scores = []
        for ability_score in self.ability_scores:
            raw_scores.append(ability_score.get_val())
            

        scores = {'str':raw_scores[0], 'dex':raw_scores[1], 'con':raw_scores[2], 'int':raw_scores[3], 'wis':raw_scores[4], 'cha':raw_scores[5]}
        print(scores)
        return scores

    def set_scores(self, new_scores:list):
        if len(new_scores) != len(self.ability_scores):
            raise SyntaxError("length mismatch")
        for ability_score, new_score in self.ability_scores, new_scores:
            ability_score.ability_score_val = new_score

#END Ability_score_block

class Health_field(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        ttk.Label(self, text="Maximum Health").grid()
        self.health_var = tk.IntVar()
        health_entry = ttk.Entry(self, width=4, textvariable=self.health_var)
        health_entry.grid()

class Level_field(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        ttk.Label(self, text="Character Level").grid()
        self.level_var = tk.IntVar()
        level_entry = ttk.Entry(self, width=4, textvariable=self.level_var)
        level_entry.grid()

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

if __name__ == '__main__':
    app = App()
    app.mainloop()