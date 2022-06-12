import json
import tkinter as tk
from tkinter import ttk, filedialog as fd
from Character import Character

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # 'widthxlength'
        self.geometry('350x450')
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

        self.initialize_Character()

    def initialize_Character(self):
        # self.model.create_character()
        NotImplemented

    def print_values(self):
        temp = self.view.window
        print(f"name: {temp.name_field.name}")
        print(f"class: {temp.class_selector.class_name}")
        print(f"level: {temp.level_field.level}")
        print(f"max health: {temp.max_health_field.max_health}")
        print(temp.score_block.scores)

    def save(self):
        view = self.view.window
        self.model.set_data(
            name=view.name_field.name,
            # name=view.name_field.get(), 
            level=view.level_field.level, 
            max_health=view.max_health_field.max_health,
            ability_scores=view.score_block.scores,
            player_class=view.class_selector.class_name)
        filepath = self.model.filepath
        name = self.model.data['name']
        #TODO check to see if there is a name collision and ask the user to confirm replacement
        with open(f"{filepath}{self.sanitize_filename(name)}.json", 'w') as outfile:
            json.dump(self.model.data, outfile)

    def load_from_file(self, filepath):
        # filepath = f"{self.model.filepath}{filename}"
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
        view.name_field.name = data['name']
        view.level_field.level = data['level']
        view.max_health_field.max_health = data['health']
        view.score_block.scores = data['ability_scores']
        view.class_selector.class_name = data['class']

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

        self.skill_block = Skills_block(self.frame)

        self.frame.grid(column=1, row=0, padx=5, pady=5)
        self.name_field.grid(padx=5, pady=5, sticky=tk.W)
        self.level_field.grid(column=1, row=0, padx=5, pady=5)
        self.max_health_field.grid(padx=5, pady=5, sticky=tk.W)
        self.score_block.grid(column=0, padx=5, pady=5)
        self.class_selector.grid()

        self.skill_block.grid(column=1, row=2)

        ttk.Button(self.frame, text="print values", command=self.button_pressed).grid()
        ttk.Button(self.frame, text="save", command=self.save_button_pressed).grid()
        ttk.Button(self.frame, text="load save", command=self.load_button_pressed).grid()


    def load_button_pressed(self):
        if self.view.controller:
            # create file selector dialog
            filename = fd.askopenfilename(initialdir="data/characters/")

            self.view.controller.load_from_file(filename)
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
            'level':0,
            'ability_scores': {
                'str':0,
                'dex':0,
                'con':0,
                'int':0,
                'wis':0,
                'cha':0
                },
            'health':None,
            'race':None,
            'skills': {
                'acrobatics': {
                    'score':'str',
                    'prof':False 
                    },
                'animal_handling': {
                    'score':'wis',
                    'prof':False
                    },
                'arcana': {
                    'score':'int',
                    'prof':False
                    },
                'athletics': {
                    'score':'str',
                    'prof':False
                    },
                'deception': {
                    'score':'cha',
                    'prof':False
                    }
            }
        }


    # skill proficiency list (eg. ('arcana', 'deception') ) use these as keys to skills dict and set 'prof' to True in each
    def set_data(self, name, ability_scores, level, player_class, max_health):
        '''method to initialize the data dict and to load from save'''
        # ability_scores = ['str', 'dex', 'con', 'int', 'wis', 'cha']
        self.data['name'] = name
        self.data['class'] = level
        self.data['ability_scores'] = ability_scores
        self.data['level'] = level
        self.data['class'] = player_class
        self.data['health'] = max_health

    def create_character(self):
        ability_scores = self.data['ability_scores']
        self.character = Character(
            strength=ability_scores['str'],
            dextertity=ability_scores['dex'],
            constitution=ability_scores['con'],
            intelligence=ability_scores['int'],
            wisdom=ability_scores['wis'],
            charisma=ability_scores['cha'],
            # playerClass=player_class,
            # Haven't yet built support for player_class specific behavior
            playerClass=None,
            maxHealth=self.data['health'],
            level=self.data['level'],
            heritage=None
            )
        return NotImplemented
# End Model


class Skills_block(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.skill_checks = [
            Skill(self, "acrobatics"),
            Skill(self, "animal handling"),
            Skill(self, "arcana"),
            Skill(self, "athletics"),
            Skill(self, "deception"),
            Skill(self, "history")
        ]

        row = 0
        for skill in self.skill_checks:
            tk.Label(self, text=skill.name).grid(column=0, padx=5, row=row, sticky=tk.NSEW)
            skill.grid(column=1, row=row, padx=5, sticky=tk.NSEW)
            tk.Label(self, textvariable=skill.skill_mod).grid(column=2, padx=2, row=row, sticky=tk.NSEW)
            # ability_score.ability_mod_label.grid(column=2, row=row, padx=5)
            row = row+1

    @property
    def proficiencies(self):
        return NotImplemented

    @proficiencies.setter
    def proficiencies(self):
        return NotImplemented

class Skill(ttk.Frame):
    def __init__(self, parent, name):
        super().__init__(parent)
        self.parent = parent
        self.name = name
        self.prof_bool = tk.BooleanVar(value=True)
        self.prof_checkbox = tk.Checkbutton(self, variable=self.prof_bool)
        self.skill_mod = tk.IntVar(value=0)
        self.prof_checkbox.grid()

    def set_mod(self, new_value):
        self.skill_mod.set(new_value)

    def set_proficient(self, is_proficient):
        self.prof_bool=is_proficient

class Ability_score(ttk.Frame):
    def __init__(self, parent, name):
        super().__init__(parent)
        self.parent = parent
        self.name = name
        # set initial value to 10 to follow D&D convention.
        self.__ability_score_val = tk.IntVar(value=10)
        self.__ability_mod_val = tk.IntVar()
        abilityscore_validate_command = (self.parent.register(self.ability_validate),
            '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.label = tk.Label(self, text=self.name)
        self.ability_score_entry = tk.ttk.Entry(self, width=4, textvariable=self.__ability_score_val, validate="key", validatecommand=abilityscore_validate_command)
        # self.ability_mod_label = tk.Label(self, textvariable=self.__ability_mod_val)
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
            self.__ability_score_val.set(0)
            # return False
        try:
            int(value_if_allowed)
            return True
        except ValueError:
            return False

    def set_empty_to_zero(self, event):
        '''Called when focus is lost to replace empty cells with 0s'''
        if self.score_value == -1:
            self.score_value = 0

    def update_ability_mod(self, event):
        '''Update ability modifier field. To be called when changes are made to the ability score.'''
        # the get() method of the tk.IntVar will throw an error if the value is set to an empty string
        try:
            ability_score = self.__ability_score_val.get()
            self.__ability_mod_val.set((ability_score - 10) // 2)
            if ability_score > 30:
                # Indicate when ability score exceeds the normal maximum value to help catch human input errors.
                self.ability_score_entry.config({"foreground":"Red"})
            else:
                self.ability_score_entry.config({"foreground":"Black"})
        except tk.TclError:
            # treat no value the same as 0 for simplicity's sake. (a score of 0 yields -5)
            self.ability_score_entry.config({"foreground":"Black"})
            self.__ability_mod_val.set(-5)

    @property
    def label_value(self):
        if self.label:
            return self.label

    @property
    def score_value(self):
        try:
            return self.__ability_score_val.get()
        except tk.TclError:
            return -1

    @property
    def mod_value(self):
        return self.__ability_mod_val.get()

    @score_value.setter
    def score_value(self, new_value):
        self.__ability_score_val.set(new_value)
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
            tk.Label(self, textvariable=ability_score.mod_value).grid(column=2, padx=10, row=row, sticky=tk.NSEW)
            # ability_score.ability_mod_label.grid(column=2, row=row, padx=5)
            row = row+1

    @property
    def scores(self):
        return {'str':self.raw_scores[0], 
                'dex':self.raw_scores[1], 
                'con':self.raw_scores[2], 
                'int':self.raw_scores[3], 
                'wis':self.raw_scores[4], 
                'cha':self.raw_scores[5]}

    @property
    def raw_scores(self):
        '''return a dict containing the abreviated score label and value(eg. 'str':15)'''
        raw_scores = []
        for ability_score in self.ability_scores:
            raw_scores.append(ability_score.score_value)
        # print(raw_scores)
        return raw_scores

    @scores.setter
    def scores(self, new_scores):
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
        __health_varidate_command = (self.parent.register(self.__health_varidate),
            '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        ttk.Label(self, text="Maximum Health").grid()
        self.__health_var = tk.IntVar()
        health_entry = ttk.Entry(self, width=4, textvariable=self.__health_var, validate="key", validatecommand=__health_varidate_command)
        health_entry.grid()

    def __health_varidate(self, action, index, value_if_allowed,
                       prior_value, text_delta, validation_type, trigger_type, widget_name):
        try:
            int(value_if_allowed)
            return True
        except ValueError:
            return False

    @property
    def max_health(self):
        try:
            return self.__health_var.get()
        except tk.TclError:
            return -1

    @max_health.setter
    def max_health(self, new_val):
        # TODO add validation to all potential values.
        self.__health_var.set(new_val)


class Level_field(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        ttk.Label(self, text="Character Level").grid()
        self.__level_var = tk.IntVar()
        level_entry = ttk.Entry(self, width=4, textvariable=self.__level_var)
        level_entry.grid()

    @property
    def level(self):
        try:
            return int(self.__level_var.get())
        except tk.TclError:
            # TODO this is clunky, I should really fix this
            return -1

    @level.setter
    def level(self, new_val):
        self.__level_var.set(new_val)


class Name_field(ttk.Frame):
    """Receive name entry"""
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.parent = parent
        
        name_validate_command = (self.parent.register(self.name_validate),
            '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        ttk.Label(self, text="character name").grid()
        # name_var should never be accessed directly
        self.__name_var = tk.StringVar()
        # updates the value of data['name'] when the name entry is changed.
        #self.__name_var.trace_add('write', update_name)
        name_entry = ttk.Entry(self, width=12, textvariable=self.__name_var, validate="key", validatecommand=name_validate_command)
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

    @property
    def name(self):
        return self.__name_var.get()

    @name.setter
    def name(self, new_name):
        self.__name_var.set(new_name)

#END Name_field

class Class_selector(ttk.Frame):
    def __init__(self, parent, player_classes) -> None:
        super().__init__(parent)
        self.parent = parent
        self.player_classes = player_classes
        
        ttk.Label(self, text="Player Class").grid()
        # label_text = tk.StringVar()
        # update_label = ttk.Label(self.parent, textvariable=label_text).grid()
        self.__class_var = tk.StringVar()
        player_class_selector = ttk.Combobox(self, textvariable=self.__class_var)
        player_class_selector.bind('<<ComboboxSelected>>', lambda *defs : player_class_selector.selection_clear())
        player_class_selector['values'] = player_classes
        player_class_selector.grid()
        player_class_selector.state(['readonly'])

    @property
    def class_name(self):
        return self.__class_var.get()

    @class_name.setter
    def class_name(self, class_from_list):
        # TODO implement some form of input sanitization or change the implementation
        #   to ensure that the set player_class is known.
        #   Although maybe the UI should be ambivilant and I should move that responsibility elsewhere?
        self.__class_var.set(class_from_list)

    # def set_current_selection(selection):
    #     if selection in player_class_list:



#END Class_selector

if __name__ == '__main__':
    app = App()
    app.mainloop()