# -*- coding: utf-8 -*-
#!/usr/bin/env python3
###############################################################################
##
## Bloodystats uses SimulationCraft to get the best secondary stat distribution
## for a set of talent combinations.
##
## Read README.txt to install/use correctly
##
## Script is written on and for Windows 10 only. I don't test it on any other 
## system.
## 
## Needs:  Python 3.5.3
##         Numpy
##         Scipy
##
## This program is provided as is. No warranity of any kind is given. Use it at
## your own risk.
##
## How to build: (this information is only relevant for the forgetful author 
## himself)
##   use powershell and 
##   pyinstaller .\Bloodystats.spec
##
##
## Questions, ideas? Hit me up on Discord:
## https://discord.gg/tFR2uvK       Channel: #Bloodystats
##                                                              Bloodmallet(EU)
###############################################################################



##-----------------------------------------------------------------------------
## Imports
##-----------------------------------------------------------------------------

## params
import argparse
## Library to get date and calculationtime for program
import datetime
## Library to look for files and create them if needed
# import os
## Settings of bloodystats
import settings
import sys

## Library with general wow information
import libraries.wow_lib as wow_lib
## Library with simc values and checks
import libraries.simc_checks as simc_checks

## Function which manages all available calculation functions
import libraries.methods.calculation_manager as calculation_manager
## Function which manages all available ouput functions
import libraries.output.output_manager as output_manager



##-----------------------------------------------------------------------------
## Functions
##-----------------------------------------------------------------------------


##
## @brief      Generates all possible talent combinations for simc depending on
##             blueprint and wow_lib.get_dps_talents
##
## @param      blueprint  The blueprint
##
## @return     List of all possible talent combinations
##
def __generate_talent_combinations(blueprint):
  if not ("x" in blueprint or "-" in blueprint):
    return [blueprint]
  data_talents = wow_lib.get_dps_talents(args.wow_class)
  pattern = ""
  for i in range(0, 7):
    if (blueprint[i] == "-" or blueprint[i] == "x") and data_talents[i] == "0":
      pattern += "0"
    else:
      pattern += blueprint[i]
  combinations = []
  for first in range(4):
    for second in range(4):
      for third in range(4):
        for forth in range(4):
          for fivth in range(4):
            for sixth in range(4):
              for seventh in range(4):
                combination = str(first) + str(second) + str(third) + str(forth) + str(fivth) + str(sixth) + str(seventh)
                add_it = True
                for i in range(7):
                  if (not (pattern[i] == "-" or pattern[i] == "x")) and not combination[i] == pattern[i]:
                    add_it = False
                  if combination[i] == "0" and (pattern[i] == "-" or pattern[i] == "x"):
                    add_it = False
                if add_it:
                  combinations += [combination]
  return combinations


##
## @brief      Generates all possible talent combinations for simc depending on
##             two_digits and wow_lib.get_dps_talents
##
## @param      two_digits  Two digits
##
## @return     List of all possible talent combinations
##
def __generate_talent_combinations_wrapper(two_digits):
  return __generate_talent_combinations("-----" + two_digits)

##
## @brief      Get talent combinations from custom_talent_combinations.simc
##
## @return     List of all talent combinations from custom_talent_combinations.simc
##
def __grab_talent_combinations():
  with open("custom_talent_combinations.simc", "r") as f:
    combination_amount = sum(1 for _ in f)
  if combination_amount == 0:
      print("No talent combination in 'custom_talent_combinations.simc' found. Please recheck settings.py or your input.")
  run = 1
  combinations = []
  with open("custom_talent_combinations.simc", "r") as talent_heap:
    for line in talent_heap:
      if line[-1:] == "\n":
        combinations.append(line[:-1])
      else:
        combinations.append(line)
  return combinations


##
## @brief      Gets the secondaries.
##
## @param      string  The string
##
## @return     The secondaries as int.
##
def __grab_secondaries(string):
  if string[-1] == '\n':
    return int(string.split("=")[1][:-1])
  else:
    return int(string.split("=")[1])


##
## @brief      Checks validity of input (args)
##
## @return     True if data is fine.
##
def is_input():
  print("Check for corrupted data.")
  load_errors = 0
  print("  Bloodystats settings:")

  print("    calculation_method\t\t", end="")
  if calculation_manager.is_calculation_method(args.calculation_method):
    print(args.calculation_method)
  else:
    print("corrupted")
    load_errors += 1

  print("    custom_character_stats\t", end="")
  if type(args.custom_character_stats) == bool:
    if args.custom_character_stats:
      print("forced on")
    else:
      print("not forced on")
  else:
    print("corrupted")
    load_errors += 1

  print("    custom_fight_style\t\t", end="")
  if type(args.custom_fight_style) == bool:
    if args.custom_fight_style:
      print("forced on")
    else:
      print("not forced on")
  else:
    print("corrupted")
    load_errors += 1

  print("    html\t\t\t", end="")
  if type(args.html) == bool:
    if args.html:
      print("forced on")
    else:
      print("not forced on")
  else:
    print("corrupted")
    load_errors += 1

  print("    output\t\t\t", end="")
  for method in args.output:
    if output_manager.is_output(method):
      print(method + " ", end="")
    else:
      print("corrupted")
      load_errors += 1
  print("")

  print("    silent_end\t\t\t", end="")
  if type(args.silent_end) == bool:
    if args.silent_end:
      print("forced on")
    else:
      print("not forced on")
  else:
    print("corrupted")
    load_errors += 1

  print("")
  print("  Char settings:")
  print("    wow_class\t\t\t", end="")
  if wow_lib.is_class(args.wow_class):
    print(args.wow_class)
  else:
    print("corrupted")
    load_errors += 1

  print("    wow_race\t\t\t", end="")
  if wow_lib.is_race(args.wow_race):
    print(args.wow_race)
  else:
    print("corrupted")
    load_errors += 1

  print("    wow_spec\t\t\t", end="")
  if wow_lib.is_spec(args.wow_spec):
    print(args.wow_spec)
  else:
    print("corrupted")
    load_errors += 1

  if not wow_lib.is_class_spec(args.wow_class, args.wow_spec):
    print("    The combination of wow_class and wow_spec is not valid.")

  print("    talents\t\t\t", end="")
  if is_talent_combination(args.talent_combination):
    print(args.talent_combination)
  else:
    print("corrupted")
    load_errors += 1

  print("    profile\t\t\t", end="")
  if simc_checks.is_profile(args.profile):
    print(args.wow_spec)
  else:
    print("corrupted")
    load_errors += 1

  print("    tier_set_bonus_2\t\t", end="")
  if type(args.tier_set_bonus_2) == bool:
    if args.tier_set_bonus_2:
      print("forced on")
    else:
      print("not forced on")
  else:
    print("corrupted")
    load_errors += 1

  print("    tier_set_bonus_4\t\t", end="")
  if type(args.tier_set_bonus_4) == bool:
    if args.tier_set_bonus_4:
      print("forced on")
    else:
      print("not forced on")
  else:
    print("corrupted")
    load_errors += 1

  print("    tier_set_number\t\t", end="")
  if simc_checks.is_tier_number(args.tier_set_number):
    print(args.tier_set_number)
  else:
    print("corrupted")
    load_errors += 1

  print("")
  print("  SimulationCraft settings:")
  print("    default_actions\t\t", end="")
  if type(args.default_actions) == bool:
    if args.default_actions:
      print("forced on")
    else:
      print("not forced on")
  else:
    print("corrupted")
    load_errors += 1

  print("    fight_style\t\t\t", end="")
  if simc_checks.is_fight_style(args.fight_style):
    print(args.fight_style)
  else:
    print("corrupted")
    load_errors += 1

  print("    iterations\t\t\t", end="")
  if simc_checks.is_iteration(args.iterations):
    print(args.iterations)
  else:
    print("corrupted")
    load_errors += 1

  print("    target_error\t\t", end="")
  if simc_checks.is_target_error(args.target_error):
    print(args.target_error)
  else:
    print("corrupted")
    load_errors += 1

  print("    threads\t\t\t", end="")
  if simc_checks.is_threads(args.threads):
    if args.threads == "":
      print("all")
    else:
      print(args.threads)
  else:
    print("corrupted")
    load_errors += 1

  print("    ptr\t\t\t\t", end="")
  if type(args.ptr) == bool:
    if args.ptr:
      print("forced on")
    else:
      print("not forced on")
  else:
    print("corrupted")
    load_errors += 1
  print("Checks are done.")
  if load_errors > 0:
    return False
  else:
    return True


##
## @brief      Gets the possible talent combinations.
##
## @return     The possible talent combinations as a list.
##
def get_talent_combinations():
  combination = []
  if args.talent_combination == "" or args.talent_combination == None:
    combinations = __grab_talent_combinations()
    for combination in combinations:
      if not is_talent_combination(combination):
        sys.exit("At least one of the talent combinations from custom_talent_combinations.simc isn't valid.")
  elif len(args.talent_combination) == 2:
    combinations = __generate_talent_combinations_wrapper(args.talent_combination)
  elif len(args.talent_combination) == 7:
    combinations = __generate_talent_combinations(args.talent_combination)
  else:
    sys.exit("Something went wrong when generating talent combinations. Please recheck your input and settings")
  return combinations

##
## @brief      Gets the secondary ratings from profile or
##             custom_character_stats.simc.
##
## @return     The secondary ratings as int.
##
def get_secondary_ratings():
  amount = 0
  path = "../profiles/Tier"
  path += args.profile[1:] + "/"
  path += args.wow_class   + "_"
  path += args.wow_spec    + "_"
  path += args.profile     + ".simc"
  if args.custom_character_stats:
    path = "custom_character_stats.simc"
  with open(path, "r") as char_values:
    for line in char_values:
      if "gear_crit_rating=" in line or "gear_haste_rating=" in line or "gear_mastery_rating=" in line or "gear_versatility_rating=" in line:
        amount += __grab_secondaries(line)
  return amount


##
## @brief      Determines if talent input from user is in a valid format.
##
## @param      talent_combination  The talent combination
##
## @return     True if talent input is valid, False otherwise.
##
def is_talent_combination(talent_combination):
  if talent_combination == None:
    return True
  if not type(talent_combination) is str:
    return False
  if talent_combination == "":
    return True
  if len(talent_combination) == 7:
    for letter in talent_combination:
      if not (letter == "0" or letter == "1" or letter == "2" or letter == "3" or letter == "-" or letter == "x"):
        return False
    return True
  elif len(talent_combination) == 2:
    for letter in talent_combination:
      if not (letter == "0" or letter == "1" or letter == "2" or letter == "3"):
        return False
    return True
  # Would've been for talent combinations that set certain rows to a value without declaring anything else. Like 42 would set the forth row to the second talent. 4253 would set 4. row to 2 and 5. to 3
  #elif len(talent_combination) % 2 == 0:
  #  for i in range(0, len(talent_combination)):
  #    if (i + 1) % 2 == 1 and not int(talent_combination[i]) in range(1,8):
  #      return False
  #    elif not int(talent_combination[i]) in range(0,4):
  #      return False
  #  return True
  else:
    return False


##-----------------------------------------------------------------------------
## Argument parser
##-----------------------------------------------------------------------------

parser = argparse.ArgumentParser(description="Program calculates best secondary stat distribution for talent combinations. - Program of Bloodmallet(EU). Questions, ideas? Hit me up on Discord: https://discord.gg/tFR2uvK #bloodystats - Version: February 2017")

## Bloodystats settings:
parser.add_argument(
  "--calculation_method", 
  nargs="?", 
  default=settings.calculation_method,
  help="Define which calculation method you want to use.")
parser.add_argument(
  "-ccs", "--custom_character_stats",
  action="store_const",
  const=True,
  default=settings.custom_character_stats,
  help="Enables custom_character_stats.simc in addition to the basic profile." )
parser.add_argument(
  "-cfs", "--custom_fight_style", 
  action="store_const", 
  const=True, 
  default=settings.custom_fight_style, 
  help="Enables custom_fight_style.simc." )
parser.add_argument(
  "--html", 
  action="store_const", 
  const=True, 
  default=settings.html, 
  help="Enable html output for SimulationCraft. (Spam your disk w00p w00p!)" )
parser.add_argument(
  "--output", 
  nargs="*", 
  default=settings.output,
  help="Define which output methods you want to use (multiple at the same time possible).")
parser.add_argument(
  "-se", "--silent_end", 
  dest="silent_end", 
  action="store_const", 
  const=True, 
  default=settings.silent_end, 
  help="Let the program terminate without user input.")

## Char settings
parser.add_argument(
  "--class", 
  nargs="?", 
  default=settings.wow_class, 
  choices=wow_lib.get_classes(),
  dest="wow_class",
  help="Name of the class of your character." )
parser.add_argument(
  "--race", 
  nargs="?", 
  default=settings.wow_race, 
  choices=wow_lib.get_races(),
  dest="wow_race",
  help="Name of the race." )
parser.add_argument(
  "--spec", 
  nargs="?", 
  default=settings.wow_spec, 
  dest="wow_spec",
  help="Name of the specialisation of your character." )
parser.add_argument(
  "--talents", "--talent_combination",
  nargs="?", 
  default=settings.talents,
  dest="talent_combination",
  help="Talentselection of the last two rows or full. E.g. 12 vs 2112332 vs 2----12 vs 2xxxxx12. Empty enables custom_talent_combinations.simc. For further information please read the README.TXT" )
parser.add_argument(
  "--profile",
  nargs="?",
  default=settings.profile,
  choices=simc_checks.get_profiles(),
  help="Determines which basic profile will be used for calculations. (example: 19M_NH)" )
parser.add_argument(
  "-t2", 
  "--tier_set_bonus_2", 
  action="store_const", 
  const=True, 
  default=settings.tier_set_bonus_2, 
  help="Enables --tier_set_number 2 piece bonus." )
parser.add_argument(
  "-t4", 
  "--tier_set_bonus_4", 
  action="store_const", 
  const=True, 
  default=settings.tier_set_bonus_4, 
  help="Enables --tier_set_number 4 piece bonus." )
parser.add_argument(
  "-tier", "--tier_set_number", 
  nargs="?", 
  default=settings.tier_set_number, 
  choices=simc_checks.get_tiers(), 
  help="Determines which tier set bonuses will be activated." )

## SimulationCraft settings
parser.add_argument(
  "--default_actions", 
  action="store_const", 
  const=True, 
  default=settings.default_actions, 
  help="Enable default_actions for SimulationCraft." )
parser.add_argument(
  "-f", "--fight_style", 
  nargs="?", 
  default=settings.fight_style,
  choices=simc_checks.get_fight_styles(), 
  help="Decides uppon the fight style. -cfs has a higher priority." )
parser.add_argument(
  "-i", 
  "--iterations", 
  nargs="?", 
  default=settings.iterations, 
  choices=["5000", "7500", "10000", "12500", "15000", "25000", "50000", "250000", "500000"], 
  help="SimulationCraft maximum iterations." )
parser.add_argument(
  "--target_error", 
  nargs="?", 
  default=settings.target_error, 
  choices=["0.5", "0.2", "0.1", "0.09", "0.08", "0.075", "0.07", "0.05", "0.0"], 
  help="Sets the target error of SimulationCraft" )
parser.add_argument(
  "--threads", 
  nargs="?", 
  default=settings.threads, 
  help="Sets the number of threads SimulationCraft will use." )
parser.add_argument(
  "--ptr", 
  action="store_const", 
  const=True, 
  default=settings.ptr, 
  help="Enable ptr calculation for SimulationCraft." )

args = parser.parse_args()



##-----------------------------------------------------------------------------
## Program start
##-----------------------------------------------------------------------------

print("Welcome to Bloodystats")
print("A project of Bloodmallet(EU)")
print("----------------------------")
if not is_input():
  sys.exit("Encountered corrupted data.")
else:
  print("Data seems fine.")

print("")
print("Getting secondary ratings\t", end="")
args.secondaries_amount = 0
args.secondaries_amount = get_secondary_ratings()
if args.secondaries_amount > 0:
  print(str(args.secondaries_amount))
else:
  print("corrupted")
  sys.exit("No secondaries were found. Program is shutting down.")

print("")
print("Generating necessary talent combinations.")
talent_combinations = get_talent_combinations()
args.combination_count = len(talent_combinations)
args.current_combination_count = 1
print("We'll have to do ", end="")
if args.combination_count > 1:
  print(str(args.combination_count) + " runs. Better start now.")
else:
  print("one run. Lazily starting now.")

simulation_start = datetime.datetime.now()
args.base_name = "{:%Y_%m_%d__%H_%M}".format(datetime.datetime.now())
args.base_name += args.fight_style + "_"
args.base_name += args.wow_class + "_"
args.base_name += args.wow_spec + "_"
args.base_name += args.wow_race

result_list = []
last_result = ()
for talent_combination in talent_combinations:
  last_result = calculation_manager.calculation_manager(args, talent_combination)
  result_list.append(last_result)
  print("Result: " + talent_combination + "\t", end="")
  print(last_result[1] + "\t\t" + last_result[2] + "\t\t" + last_result[3] + "\t\t" + last_result[4] + "\t\t" + last_result[5])
  args.current_combination_count += 1
  if output_manager.output_manager(args, last_result, True):
    print("Log sucessfull.")
  else:
    print("Log failed.")
  print("")
simulation_end = datetime.datetime.now()
print("Calculation took " + str(simulation_end - simulation_start))
print("Generating output.")
if output_manager.output_manager(args, result_list, False):
  print("Output sucessfull.")
else:
  print("Output failed.")
print("Bloodystats ends now. Thank you for using it.")
print("\t\twritten by Bloodmallet(EU)")
if not args.silent_end:
  endsign = input("Press Enter to terminate...")
  print("The End")
