import json
import tkinter as tk
from tkinter import ttk
from Character import Character

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # 'widthxlength'
        self.geometry('300x450')
        self.title("Edit Character")

        model = Model()
        view = View(self)
        controller = Controller(model, view)

        view.set_controller(controller)


class View(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.controller:Controller = None
        self.window = Main_Window(parent=parent, view=self)

    def set_controller(self, controller):
        self.controller = controller

# End View

class Controller:
    def __init__(self, model, view) -> None:
        self.model:Model = model
        self.view:View = view

    def print_values(self):
        temp = self.view.window
        print(f"name: {temp.name_field.get()}")
        print(f"class: {temp.class_selector.get()}")
        print(f"level: {temp.level_field.get()}")
        print(f"max health: {temp.max_health_field.get()}")
        print(temp.score_block.get_scores())

    def save(self):
        view = self.view.window
        self.model.set_data(
            name=view.name_field.get(), 
            level=view.level_field.get(), 
            max_health=view.max_health_field.get(), 

            ability_scores=view.score_block.get_scores(),
            
            player_class=view.class_selector.get())
        filepath = self.model.filepath
        name = self.model.data['name']
        #TODO check to see if there is a name collision and ask the user to confirm replacement
        with open(f"{filepath}{self.sanitize_filename(name)}.json", 'w') as outfile:
            json.dump(self.model.data, outfile)

    def load_from_file(self, filename):
        filepath = f"{self.model.filepath}{filename}"
        # try:
        #     with open(filepath) as json_file:
        #         self.model.data = json.load(json_file)
        # except FileNotFoundError:
        #     raise
        with open(filepath) as json_file:
            self.model.data = json.load(json_file)
        self.update_fields()

    def update_fields(self):
        view = self.view.window
        data = self.model.data
        view.name_field.set(data['name'])
        view.level_field.set(data['level']) 
        view.max_health_field.set(data['health']) 
        view.score_block.set_scores(data['ability_scores'])
        view.class_selector.set(data['class'])

    def sanitize_filename(self, name):
        #check if name is empty
        if not name:
            raise Exception("name must not be empty")
        #Remove preceding whitespace, replace whitespace with underscores, cast to lower case
        filename = name.lstrip().replace(" ", "_").lower()
        return filename
        
# End Controller

class Main_Window:
    # def __init__(self, parent, controller):
    def __init__(self, parent, view):

        self.view:View = view
        self.parent = parent
        self.frame = tk.Frame(self.parent)
        self.name_field = Name_field(self.frame)
        self.level_field = Level_field(self.frame)
        self.max_health_field = Health_field(self.frame)
        self.score_block = Ability_score_block(self.frame)
        # TODO player classes list to Model or Controller object
        player_classes = ('Artificer', 'Barbarian', 'Bard', 'Cleric', 'Druid', 'Fighter', 'Monk', 'Paladin', 'Ranger', 'Rogue', 'Sorcerer', 'Warlock', 'Wizard')
        self.class_selector = Class_selector(self.frame, player_classes)

        self.frame.grid(column=1, row=0, padx=5, pady=5)
        self.name_field.grid(padx=5, pady=5, sticky=tk.W)
        self.level_field.grid(column=1, row=0, padx=5, pady=5)
        self.max_health_field.grid(padx=5, pady=5, sticky=tk.W)
        self.score_block.grid(padx=5, pady=5)
        self.class_selector.grid()

        ttk.Button(self.frame, text="print values", command=self.button_pressed).grid()
        ttk.Button(self.frame, text="save", command=self.save_button_pressed).grid()
        ttk.Button(self.frame, text="load save", command=self.load_button_pressed).grid()


    def load_button_pressed(self):
        if self.view.controller:
            # THIS IS A PLACEHOLDER, OH GOD PLEASE ADD A FILE SELECTOR
            # TODO add a file selector
            self.view.controller.load_from_file("beepo.json")
        else:
            raise Exception("can't load, can't find controller. Where'd you put it last?")

    def save_button_pressed(self):
        if self.view.controller:
            self.view.controller.save()
        else:
            raise Exception("can't save: no controller, that's weird")

    def button_pressed(self):
        if self.view.controller:
            self.view.controller.print_values()
        else:
            raise Exception


class Model:
    '''Model should not require knowledge of other components. Is responsible for storage and maybe data validation'''
    def __init__(self) -> None:
        self.filepath = "data/characters/"
        self.character:Character = None
        self.data = {
            'name':None,
            'class':None,
            'level':None,
            'ability_scores': {
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

    def set_data(self, name, ability_scores, level, player_class, max_health):
        '''method to initialize the data dict and to load from save'''
        # ability_scores = ['str', 'dex', 'con', 'int', 'wis', 'cha']
        self.data['name'] = name
        self.data['class'] = level
        self.data['ability_scores'] = ability_scores
        self.data['level'] = level
        self.data['class'] = player_class
        self.data['health'] = max_health

    def create_character(self, stat_array, level, player_class, max_health):

        self.character = Character(
            strength=stat_array['str'],
            dextertity=stat_array['dex'],
            constitution=stat_array['con'],
            intelligence=stat_array['int'],
            wisdom=stat_array['wis'],
            charisma=stat_array['cha'],
            playerClass=player_class, maxHealth=max_health,
            level=level,
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
        # set default value to 10 to follow D&D convention.
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
        # -> Disallow any non-number characters.    
        self.ability_score_entry.config({"foreground":"Black"})
        # allow empty value so that user can use backspace to get to the beginning before entering new value.     
        if not value_if_allowed:
            return True
        # otherwise only allow values that can be converted to an int
        if len(value_if_allowed)>1 and not value_if_allowed.lstrip('0') == value_if_allowed:
            self.ability_score_val.set(0)
            # return False
        try:
            int(value_if_allowed)
            return True
        except ValueError:
            return False

    def set_empty_to_zero(self, event):
        '''Called when focus is lost to replace empty cells with 0s'''
        if self.get_val() == -1:
            self.set_val(0)

    def update_ability_mod(self, event):
        '''Update ability modifier field. To be called when changes are made to the ability score.'''
        # the get() method of the tk.IntVar will throw an error if the value is set to an empty string
        try:
            ability_score = self.ability_score_val.get()
            self.ability_mod_val.set((ability_score - 10) // 2)
            if ability_score > 30:
                # Indicate when ability score exceeds the normal maximum value to help catch human input errors.
                self.ability_score_entry.config({"foreground":"Red"})
            else:
                self.ability_score_entry.config({"foreground":"Black"})
        except tk.TclError:
            # treat no value the same as 0 for simplicity's sake. (a score of 0 yields -5)
            self.ability_score_entry.config({"foreground":"Black"})
            self.ability_mod_val.set(-5)

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
        self.update_ability_mod(None)

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
        '''return a dict containing the abreviated score label and value(eg. 'str':15)'''
        raw_scores = []
        for ability_score in self.ability_scores:
            raw_scores.append(ability_score.get_val())
        scores = {'str':raw_scores[0], 'dex':raw_scores[1], 'con':raw_scores[2], 'int':raw_scores[3], 'wis':raw_scores[4], 'cha':raw_scores[5]}
        # print(raw_scores)
        return scores
        # return raw_scores

    def set_scores(self, new_scores):
        # if new_scores is neither a list or a dict, raise error
        if not isinstance(new_scores, list):
            if isinstance(new_scores, dict):
                new_scores = list(new_scores.values())
            else:
                raise TypeError("expected list or dict")
        for i in range(6):
                self.ability_scores[i].set_val(new_scores[i])


#END Ability_score_block

class Health_field(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        health_validate_command = (self.parent.register(self.health_validate),
            '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        ttk.Label(self, text="Maximum Health").grid()
        self.health_val = tk.IntVar()
        health_entry = ttk.Entry(self, width=4, textvariable=self.health_val, validate="key", validatecommand=health_validate_command)
        health_entry.grid()

    def health_validate(self, action, index, value_if_allowed,
                       prior_value, text_delta, validation_type, trigger_type, widget_name):
        try:
            int(value_if_allowed)
            return True
        except ValueError:
            return False

    def get(self):
        try:
            return self.health_val.get()
        except tk.TclError:
            return -1

    def set(self, new_val):
        # TODO add validation to all potential values.
        self.health_val.set(new_val)


class Level_field(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        ttk.Label(self, text="Character Level").grid()
        self.level_var = tk.IntVar()
        level_entry = ttk.Entry(self, width=4, textvariable=self.level_var)
        level_entry.grid()

    def get(self):
        try:
            return int(self.level_var.get())
        except tk.TclError:
            return -1

    def set(self, new_val):
        self.level_var.set(new_val)


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

    def get(self):
        return self.name_var.get()
    
    def set(self, new_name):
        self.name_var.set(new_name)

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

    def get(self):
        return self.class_var.get()

    def set(self, class_from_list):
        # TODO implement some form of input sanitization
        self.class_var.set(class_from_list)

    # def set_current_selection(selection):
    #     if selection in player_class_list:



#END Class_selector

if __name__ == '__main__':
    app = App()
    app.mainloop()