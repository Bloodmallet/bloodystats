#!python3
import subprocess


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
def sim_secondaries(args, talent_combination, crit_rating, haste_rating, mastery_rating, versatility_rating):
  # TODO: switch depending on OS
  argument = "../simc.exe "

  if args.ptr:
    argument += "ptr=1 "

  argument += "iterations=" + args.iterations + " "
  argument += "target_error=" + args.target_error + " "
  argument += "fight_style=" + args.fight_style + " "
  argument += "fixed_time=1 "
  if args.html:
    argument += "html=" + args.base_name + ".html "

  if args.default_actions:
    argument += "default_actions=1 "

  argument += "threads=" + args.threads + " "
  argument += args.wow_class + "_" + args.wow_spec + "_" + args.profile + ".simc "

  if args.custom_character_stats:
    argument += "custom_character_stats.simc "

  argument += "race=" + args.wow_race + " "
  argument += "talents=" + talent_combination + " "

  if args.custom_fight_style:
    argument += "custom_fight_style.simc "

  argument += "default_skill=1.0 "
  argument += "calculate_scale_factors=0 "
  argument += "log=0 "

  argument += "gear_crit_rating=" + str(crit_rating) + " "
  argument += "gear_haste_rating=" + str(haste_rating) + " "
  argument += "gear_mastery_rating=" + str(mastery_rating) + " "
  argument += "gear_versatility_rating=" + str(versatility_rating) + " "

  if args.tier_set_bonus_2:
    argument += "set_bonus=tier" + args.tier_set_number + "_2pc=1 "
  if args.tier_set_bonus_4:
    argument += "set_bonus=tier" + args.tier_set_number + "_4pc=1 "

  startupinfo = subprocess.STARTUPINFO()
  startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

  simulation = subprocess.run(
    argument, 
    stdout=subprocess.PIPE, 
    stderr=subprocess.STDOUT, 
    universal_newlines=True, 
    startupinfo=startupinfo
  )

  owndps = True
  dps = -1
  for line in simulation.stdout.splitlines():
    if "DPS:" in line and owndps:
      owndps = False
      dps = int(line.split()[1].split(".")[0])
  return dps
