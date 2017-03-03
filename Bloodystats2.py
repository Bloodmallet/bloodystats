#!python3
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
import os
## Settings of bloodystats
import settings
## Library to use command line
import subprocess

## Library with general wow information
import libraries.wow_lib as wow_lib
import libraries.simc_checks as simc_checks




##-----------------------------------------------------------------------------
## Functions
##-----------------------------------------------------------------------------


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
## @brief      Generates all possible talent combinations for simc
##
## @return     List of all possible talent combinations
##
def generate_talent_input():
  talents = []
  talents += [""]
  for i in range(1, 4):
    for j in range(1, 4):
      talents += [str(i) + str(j)]
  for first in range(4):
    for second in range(4):
      for third in range(4):
        for forth in range(4):
          for fivth in range(4):
            for sixth in range(4):
              for seventh in range(4):
                talents += [str(first) + str(second) + str(third) + str(forth) + str(fivth) + str(sixth) + str(seventh)]
  return talents


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
def is_talent_input(talent_combination):
  if not type(talent_combination) is str:
    return False
  if talent_combination is "":
    return True
  if len(talent_combination) == 2 or len(talent_combination) == 7:
    for letter in talent_combination:
      if not (letter is "0" or letter is "1" or letter is "2" or letter is "3" or letter is "-" or letter is "x"):
        return False
    return True
  elif len(talent_combination) % 2 == 0:
    for i in range(0, len(talent_combination)):
      if (i + 1) % 2 == 1 and not int(talent_combination[i]) in range(1,8):
        return False
      elif not int(talent_combination[i]) in range(0,4):
        return False
    return True
  else:
    return False

##
## @brief      Calls SimulationCraft to get dps value.
##
## @param      talent_combination  The talent combination
## @param      crit_rating         The crit rating
## @param      haste_rating        The haste rating
## @param      mastery_rating      The mastery rating
## @param      versatility_rating  The versatility rating
##
## @return     DPS as s, "-1" if error
##
def sim_dps(talent_combination, crit_rating, haste_rating, mastery_rating, versatility_rating):
  argument = "../simc.exe "

  if args.ptr:
    argument += "ptr=1 "

  argument += "iterations=" + args.iterations + " "
  argument += "target_error=" + args.target_error + " "
  argument += "fight_style=" + args.fight_style + " "
  argument += "fixed_time=1 "

  if args.default_actions:
    argument += "default_actions=1 "

  argument += "threads=" + args.threads + " "
  argument += args.wow_class + "_" + args.wow_spec + "_" + args.profile + ".simc "

  if args.custom_character_stats:
    argument += "custom_character_stats.simc "

  argument += "race=" + args.wow_race + " "
  argument += "talents=" + talent_combination + " "
  argument += "fight_style=" + args.fight_style + " "

  if args.custom_fight_style:
    argument += "custom_fight_style.simc "

  argument += "gear_crit_rating=" + crit_rating + " "
  argument += "gear_haste_rating=" + haste_rating + " "
  argument += "gear_mastery_rating=" + mastery_rating + " "
  argument += "gear_versatility_rating=" + versatility_rating " "

  if args.tier_set_bonus_2:
    argument += "set_bonus=tier" + args.tier_number + "_2pc=1 "
  if args.tier_set_bonus_4:
    argument += "set_bonus=tier" + args.tier_number + "_4pc=1 "

  simulation = subprocess.run(argument, stdout=subprocess.PIPE, universal_newlines=True)
  owndps = True
  dps = "-1"
  for line in simulation.stdout.splitlines():
    if "DPS:" in line and owndps:
      owndps = False
      dps = line.split()[1]
  return dps



##-----------------------------------------------------------------------------
## Argument parser
##-----------------------------------------------------------------------------

parser = argparse.ArgumentParser(description="Program calculates best secondary stat distribution for talent combinations. - Program of Bloodmallet(EU). Questions, ideas? Hit me up on Discord: https://discord.gg/tFR2uvK #bloodystats - Version: February 2017")

## Bloodystats settings:
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
  "-html", 
  action="store_const", 
  const=True, 
  default=settings.html, 
  help="Enable html output for SimulationCraft. (Spam your disk w00p w00p!)" )
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
  help="Name of the race." )
parser.add_argument(
  "--spec", 
  nargs="?", 
  default=settings.wow_spec, 
  dest="wow_spec",
  help="Name of the specialisation of your character." )
parser.add_argument(
  "--talents", 
  nargs="?", 
  default=settings.talents,
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
  "-tier", "--tier_number", 
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
  "-f", "--fight_type", 
  nargs="?", 
  default=settings.fight_type, 
  choices=simc_checks.get_fight_styles(), 
  help="Decides uppon the fight type. -cfs has a higher priority." )
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
  "-ptr", 
  action="store_const", 
  const=True, 
  default=settings.ptr, 
  help="Enable ptr calculation for SimulationCraft." )

args = parser.parse_args()





##-----------------------------------------------------------------------------
## Program start
##-----------------------------------------------------------------------------
