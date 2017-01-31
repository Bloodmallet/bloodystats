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
##  your own risk.
##
## How to build: This information is only relevant for forgetful author himself
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
## @brief      Generates all possible talent combinations
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


def sim_dps(talent_combination, crit, haste, mastery, versatility):
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
  "-class", 
  nargs="?", 
  default=settings.wow_class, 
  choices=wow_lib.get_classes(), 
  help="Name of the class of your character." )
parser.add_argument(
  "-race", 
  nargs="?", 
  default=settings.wow_race, 
  choices=wow_lib.get_races(), 
  help="Name of the race." )
parser.add_argument(
  "-spec", 
  nargs="?", 
  default=settings.wow_spec, 
  help="Name of the specialisation of your character." )
parser.add_argument(
  "-talents", 
  nargs="?", 
  default=settings.talents, 
  choices=generate_talent_input(), 
  help="Talentselection of the last two rows or full. E.g. 12 or 33 vs 2112332. Empty enables custom_talent_combinations.simc." )

parser.add_argument(
  "-p", "--profile", 
  nargs="?", 
  default=settings.profile, 
  choices=simc_checks.get_profiles(), 
  help="Determines which basic profile will be used for calculations." )
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
  help="Decides uppon the fight type. Will be overwritten by -cfs." )
parser.add_argument(
  "-i", 
  "--iterations", 
  nargs="?", 
  default=settings.iterations, 
  choices=["5000", "7500", "10000", "12500", "15000", "17500", "20000", "25000", "50000", "250000"], 
  help="SimulationCraft maximum iterarions." )
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

