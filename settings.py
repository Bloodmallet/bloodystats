## File to store base settings.
## If you want to call Bloodystats without parameters
## or always with the same settings, just edit this
## file to contain your wanted values.
 


# Bloodystats settings:
calculation_method     = "differential_evolution"
custom_character_stats = False
custom_fight_style     = False
html                   = False
output                 = ["txt"]
silent_end             = False              # terminates without user input

 
# Char settings:
wow_class = "shaman"
wow_race  = "draenei"
wow_spec  = "elemental"
talents   = "3002332"             # "" - empty, two digits (11 to 33) or whole talent combination

profile          = "T20M"
tier_set_bonus_2 = False
tier_set_bonus_4 = False
tier_set_number  = "20"

lower_bound_crit        = "2000"
lower_bound_haste       = "2000"
lower_bound_mastery     = "2000"
lower_bound_versatility = "1500"
upper_bound             = "13500"


# SimulationCraft settings:
simc_path       = "../simc.exe"   # don't touch this one, unless you know what you're doing
default_actions = False           # set to False if you want to test your own apl in custom_character_stats...make sure to activate that too
fight_style     = "patchwerk"     # your usual simc fight styles
iterations      = "250000"
target_error    = "0.1"           # simulation terminates when it reaches this target error or iterations, whatever triggers first. target error defines other accuracies too
threads         = ""              # how many threads simc is going to use, empty results in using all
ptr             = False           # use ptr data?