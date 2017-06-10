#!python3
import subprocess
import sys


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
def sim_secondaries( args, talent_combination, crit_rating, haste_rating, mastery_rating, versatility_rating ):
  argument = [ args.simc_path ]

  if args.ptr:
    argument.append( "ptr=1 " )

  argument.append( "iterations=" + args.iterations )
  argument.append( "target_error=" + args.target_error )
  argument.append( "fight_style=" + args.fight_style )
  argument.append( "fixed_time=1" )
  if args.html:
    argument.append( "html=" + args.base_name + ".html" )

  if args.default_actions:
    argument.append( "default_actions=1" )

  argument.append( "threads=" + args.threads )
  argument.append( args.wow_class + "_" + args.wow_spec + "_" + args.profile + ".simc" )

  if args.custom_character_stats:
    argument.append( "custom_character_stats.simc" )

  argument.append( "race=" + args.wow_race )
  argument.append( "talents=" + talent_combination )

  if args.custom_fight_style:
    argument.append( "custom_fight_style.simc" )

  argument.append( "default_skill=1.0" )
  argument.append( "calculate_scale_factors=0" )
  argument.append( "log=0" )

  argument.append( "gear_crit_rating=" + str(crit_rating) )
  argument.append( "gear_haste_rating=" + str(haste_rating) )
  argument.append( "gear_mastery_rating=" + str(mastery_rating) )
  argument.append( "gear_versatility_rating=" + str(versatility_rating) )

  if args.tier_set_bonus_2:
    argument.append( "set_bonus=tier" + args.tier_set_number + "_2pc=1" )
  if args.tier_set_bonus_4:
    argument.append( "set_bonus=tier" + args.tier_set_number + "_4pc=1" )

  # should prevent additional empty windows popping up...on win32 systems without breaking different OS
  if sys.platform == 'win32':
    # call simulationcraft in the background. grab output for processing and get dps value
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    simulation = subprocess.run(
      argument, 
      stdout=subprocess.PIPE, 
      stderr=subprocess.STDOUT, 
      universal_newlines=True, 
      startupinfo=startupinfo
    )
  else:
    simulation = subprocess.run(argument, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

  owndps = True
  dps = -1
  for line in simulation.stdout.splitlines():
    if "DPS:" in line and owndps:
      owndps = False
      dps = int(line.split()[1].split(".")[0])
  return dps
