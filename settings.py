## File to store base settings.
## If you want to call Bloodystats without parameters
## or always with the same settings, just edit this
## file to contain your wanted values.
 


# Bloodystats settings:
calculation_method = "differential_evolution"
custom_character_stats = False
custom_fight_style = False
html = False
output = ["txt"]
silent_end = False              # terminates without user input

 
# Char settings:
wow_class = "shaman"
wow_race  = "draenei"
wow_spec  = "elemental"
talents = "3002332" # "" - empty, two digits (11 to 33) or whole talent combination

profile = "T19M_NH"
tier_set_bonus_2 = False
tier_set_bonus_4 = False
tier_set_number = "19"

lower_bound_crit = "2000"
lower_bound_haste = "2000"
lower_bound_mastery = "2000"
lower_bound_versatility = "1500"

upper_bound = "12500"


# SimulationCraft settings:
default_actions = False
fight_style = "patchwerk"
iterations = "250000"
target_error = "0.1"
threads = ""
ptr = False