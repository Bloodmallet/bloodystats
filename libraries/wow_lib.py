# -*- coding: utf-8 -*-
## Utility file for class specialisations
## Contains wow class names, spec names, dps talent rows

__classes_data = {
  "Death_Knight": {
    "talents": "1110011",
    "specs": {
      "Blood":  { "role": "melee", "stat": "str" },
      "Frost":  { "role": "melee", "stat": "str" },
      "Unholy": { "role": "melee", "stat": "str" }
    }
  },
  "Demon_Hunter": {
    "talents": "1110111",
    "specs": {
      "Havoc":    { "role": "melee", "stat": "agi" },
      "Vengance": { "role": "melee", "stat": "agi" }
    }
  },
  "Druid": {
    "talents": "1000111",
    "specs": { 
      "Balance":  { "role": "ranged", "stat": "int" },
      "Feral":    { "role": "melee",  "stat": "agi" },
      "Guardian": { "role": "melee",  "stat": "agi" }
    }
  },
  "Hunter": {
    "talents": "1101011",
    "specs": {
      "Beast_Mastery": { "role": "ranged", "stat": "agi" },
      "Marksmanship":  { "role": "ranged", "stat": "agi" },
      "Survival":      { "role": "melee",  "stat": "agi" }
    }
  },
  "Mage": {
    "talents": "1011011",
    "specs": {
      "Arcane": { "role": "ranged", "stat": "int" },
      "Fire":   { "role": "ranged", "stat": "int" },
      "Frost":  { "role": "ranged", "stat": "int" }
    }
  },
  "Monk": {
    "talents": "1010011",
    "specs": {
      "Brewmaster": { "role": "melee", "stat": "agi" },
      "Windwalker": { "role": "melee", "stat": "agi" }
    }
  },
  "Paladin": {
    "talents": "1101001",
    "specs": {
      "Protection":  { "role": "melee", "stat": "str" },
      "Retribution": { "role": "melee", "stat": "str" }
    }
  },
  "Priest": {
    "talents": "1001111",
    "specs": {
      "Shadow": { "role": "ranged", "stat": "int" }
    }
  },
  "Rogue": {
    "talents": "1110111",
    "specs": {
      "Assassination": { "role": "melee", "stat": "agi" },
      "Outlaw":        { "role": "melee", "stat": "agi" },
      "Subtlety":       { "role": "melee", "stat": "agi" }
    }
  },
  "Shaman": {
    "talents": "1001111",
    "specs": {
      "Elemental":   { "role": "ranged", "stat": "int" },
      "Enhancement": { "role": "melee",  "stat": "agi" }
    }
  },
  "Warlock": {
    "talents": "1101011",
    "specs": {
      "Affliction":  { "role": "ranged", "stat": "int" },
      "Demonology":  { "role": "ranged", "stat": "int" },
      "Destruction": { "role": "ranged", "stat": "int" }
    }
  },
  "Warrior": {
    "talents": "1010111",
    "specs": {
      "Arms":       { "role": "melee", "stat": "str" },
      "Fury":       { "role": "melee", "stat": "str" },
      "Protection": { "role": "melee", "stat": "str" }
    }
  }
}

__races = {
  "alliance": {
    "draenei":  (),
    "dwarf":    (),
    "gnome":    (),
    "human":    (),
    "nightelf": (),
    "pandaren": (),
    "worgen":   ()
  },
  "horde": {
    "bloodelf": (),
    "goblin":   (),
    "orc":      (),
    "pandaren": (),
    "tauren":   (),
    "troll":    (),
    "undead":   ()
  }
}

##
## @brief      Gets the wow classes.
##
## @return     The classes list.
##
def get_classes():
  classes = []
  for wow_class in __classes_data:
    classes.append(wow_class)
  return classes


##
## @brief      Gets the races.
##
## @return     The races lists.
##
def get_races():
  races = []
  for faction in __races:
    for race in __races[faction]:
      races.append(race)
  return races


##
## @brief      Gets the role from class and spec.
##
## @param      wow_class  The class name as string
## @param      wow_spec   The specifier name as string
##
## @return     The role as string.
##
def get_role(wow_class, wow_spec):
  return __classes_data[wow_class]["specs"][wow_spec]["role"]


##
## @brief      Gets the main stat like agi, str or int.
##
## @param      wow_class  The class name as string
## @param      wow_spec   The specifier name as string
##
## @return     The main stat as string.
##
def get_stat(wow_class, wow_spec):
  return __classes_data[wow_class]["specs"][wow_spec]["stat"]


##
## @brief      Gets the dps talents. 0-no dps row, 1-dps row
##
## @param      wow_class  The class name
## @param      wow_spec   For people who think spec is important...it isn't
##
## @return     The dps talents as string.
##
def get_dps_talents(wow_class, wow_spec=""):
  return __classes_data[wow_class]["talents"]


##
## @brief      Gets the specs of a class.
##
## @param      wow_class  The class name
##
## @return     The specs as a list.
##
def get_specs(wow_class):
  spec_collection = []
  for spec in __classes_data[wow_class]["specs"]:
    spec_collection.append(spec)
  return spec_collection


##
## @brief      Determines if class is a wow class.
##
## @param      wow_class  The class name
##
## @return     True if class, False otherwise.
##
def is_class(wow_class):
  for base_class in get_classes():
    if wow_class.lower() == base_class.lower():
      return True
  return False


##
## @brief      Determines if race.
##
## @param      race  The race
##
## @return     True if race, False otherwise.
##
def is_race(race):
  if race in get_races():
    return True
  return False


##
## @brief      Determines if specis of class.
##
## @param      wow_spec   The specifier name
##
## @return     True if spec exists in wow, False otherwise.
##
def is_spec( wow_spec ):
  spec_list = []
  classes = get_classes()
  for wow_class in classes:
    specs = get_specs( wow_class )
    for spec in specs:
      spec_list.append( spec )
  for spec in spec_list:
    if wow_spec.lower() == spec.lower():
      return True
  return False


##
#-------------------------------------------------------------------------------------
# Higher functions
#-------------------------------------------------------------------------------------
##


##
## @brief      Gets the role and main stat.
##
## @param      wow_class  The class name as string
## @param      wow_spec   The specifier name as string
##
## @return     List of [role, main_stat]
##
def get_role_stat(wow_class, wow_spec):
  return [get_role(wow_class, wow_spec), get_stat(wow_class, wow_spec)]


##
## @brief      Gets the role, main_stat and dps_talent_rows.
##
## @param      wow_class  The wow class
## @param      wow_spec   The wow specifier
##
## @return     The specifier information.
##
def get_spec_info(wow_class, wow_spec):
  return [
    get_role(wow_class, wow_spec), 
    get_stat(wow_class, wow_spec), 
    get_dps_talents(wow_class)
  ]


##
## @brief      Gets the main stat and role
##
## @param      wow_class  The class name as string
## @param      wow_spec   The specifier name as string
##
## @return     List of [main_stat, role]
##
def get_stat_role(wow_class, wow_spec):
  return [
    get_stat(wow_class, wow_spec),
    get_role(wow_class, wow_spec)
  ]


##
## @brief      Determines if class and spec are correct and fit each other.
##
## @param      wow_class  The wow class
## @param      wow_spec   The wow specifier
##
## @return     True if class specifier, False otherwise.
##
def is_class_spec(wow_class, wow_spec):
  if is_class(wow_class):
    if is_spec(wow_spec):
      for spec in get_specs(wow_class):
        if wow_spec.lower() == spec.lower():
          return True
  return False


##
## @brief      Determines if dps talent combination fits data.
##
## @param      talent_combination  The talent combination
## @param      wow_class           The wow class
##
## @return     True if dps talent combination fits, False otherwise.
##
def is_dps_talent_combination(talent_combination, wow_class):
  for i in range(0, 7):
    if talent_combination[i] == "0" and __classes_data[wow_class]["talents"][i] == "1":
      return False
    elif not talent_combination[i] == "0" and __classes_data[wow_class]["talents"][i] == "0":
      return False
  return True


##
## @brief      Simple data check
##
## @return     True if data doesn't have obvious flaws, False otherwise.
##
def __validity_check():
  for wow_class in __classes_data:
    for spec in get_specs(wow_class):
      if (get_role(wow_class, wow_spec) == "ranged" and get_stat(wow_class, wow_spec) == "str") or (get_role(wow_class, wow_spec) == "melee" and get_stat(wow_class, wow_spec) == "int"):
        return False
  return True