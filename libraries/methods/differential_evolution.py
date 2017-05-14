from scipy.optimize import differential_evolution
import libraries.methods.sim_it as sim_it



##
## @brief      Generates secondaries.
##
## @param      args        The arguments of the run
## @param      rng_values  Generated values by differential evolution organized
##                         as a list, 0 for crit, 1 for haste, 2 for mastery 3
##                         for vers
##
## @return     List of the four secondary ratings as str
##
def __generate_secondaries(args, rng_values):
  available_secondaries = args.secondaries_amount
  available_secondaries -= int(args.lower_bound_crit)
  available_secondaries -= int(args.lower_bound_haste)
  available_secondaries -= int(args.lower_bound_mastery)
  available_secondaries -= int(args.lower_bound_versatility)

  secondaries = __normalize(rng_values, available_secondaries)

  #apply lowerbounds
  secondaries = __apply_lower_bounds(args, secondaries)

  #apply upper bound / reshuffle values
  secondaries = __apply_upper_bound(args, secondaries)

  return secondaries


##
## @brief      Adds lower bounds to secondaries
##
## @param      args         The arguments of the run
## @param      secondaries  The secondaries
##
## @return     List of secondaries as str
##
def __apply_lower_bounds(args, secondaries):
  secondaries[0] = str(int(secondaries[0] + int(args.lower_bound_crit)))
  secondaries[1] = str(int(secondaries[1] + int(args.lower_bound_haste)))
  secondaries[2] = str(int(secondaries[2] + int(args.lower_bound_mastery)))
  secondaries[3] = str(int(secondaries[3] + int(args.lower_bound_versatility)))
  return secondaries


##
## @brief      Counts the number of fixated (True) elements.
##
## @param      fixated_list  The fixated list
##
## @return     Number of fixated.
##
def __count_fixated(fixated_list):
  counter = 0
  for fixated in fixated_list:
    if fixated:
      counter = counter + 1
  return counter


##
## @brief      Applies the upper bound to secondaries
##
## @param      args         The arguments of the run
## @param      secondaries  The secondaries
##
## @return     Returns a list of the secondaries as str
##
def __apply_upper_bound(args, secondaries):

  fixated = [False, False, False, False]
  fixated_counter = 0
  something_is_not_quite_right = True

  while something_is_not_quite_right:
    something_is_not_quite_right = False
    for i in range(0, 4):
      if int(secondaries[i]) > int(args.upper_bound):
        something_is_not_quite_right = True
        overflow = int(secondaries[i]) - int(args.upper_bound)
        if __count_fixated(fixated) == 3:
          print("Somehow the upper limit secondary distribution failed. All values had to be adjusted to be lower than the upper limit...")
          return secondaries
        # code for equal redistribution of overflow
        for j in range(0, 4):
          if j != i and not fixated[j]:
            secondaries[j] = str(int(secondaries[j]) + int(overflow / (3 - fixated_counter)))

        # code for unequal redistribution of overflow
        #fractional_sum = 0.0
        #for j in range(0, 4):
        #  if j != i:
        #    fractional_sum += secondaries[j]
        #for j in range(0, 4):
        #  if j != i:
        #    if fractional_sum == 0.0:
        #      secondaries[j] = 0.0
        #    else:
        #      secondaries[j] += overflow * secondaries[j] / fractional_sum
        secondaries[i] = args.upper_bound
        fixated[i] = True
        fixated_counter = fixated_counter + 1
  return secondaries


##
## @brief      Normalizes four rng_values (so their addition results in
##             secondaries_amount)
##
## @param      rng_values     Generated rng_values by differential evolution
##                            organized as a list, 0 for crit, 1 for haste, 2
##                            for mastery 3 for vers
## @param      secondary_sum  Sum of all secondaries - int
##
## @return     List of four secondary rng_values as strings
##
def __normalize(rng_values, secondary_sum):
  manipulator = rng_values[0] + rng_values[1] + rng_values[2] + rng_values[3]
  ## no rng_values anywhere isn't allowed, so an even distribution will be returned
  if not manipulator > 0.0:
    for i in range(0, 4):
      rng_values[i] = str(secondary_sum / 4.0)
    return rng_values

  ## normalize
  for i in range(0, 4):
    rng_values[i] = rng_values[i] / manipulator

  ## apply secondaries
  for i in range(0, 4):
    temp = 0.0
    temp = rng_values[i] * secondary_sum
    #rng_values[i] = str(int(temp.item()))
    rng_values[i] = str(int(temp))
  return rng_values


##
## @brief      Function used by differential evolution to create correct input
##
## @param      bounds              The bounds (crit, haste, mastery, vers)
## @param      talent_combination  The talent combination
##
## @return     negative dps
##
def __differential_evolution_catcher(bounds, *arguments):
  args, talent_combination = arguments
  crit, haste, mastery, vers = __generate_secondaries(args, bounds)
  dps = sim_it.sim_secondaries(args, talent_combination, crit, haste, mastery, vers)
  # TODO: Add and option to hide/show this
  print("  " + 
    str(args.current_combination_count) + "/" + str(args.combination_count) + "\t" + 
    talent_combination + "\t\t" + 
    "dps: " + str(dps) + "\t" + 
    "c:" + str(int(crit)) + "\t" + 
    "h:" + str(int(haste.item())) + "\t" + 
    "m:" + str(int(mastery.item())) + "\t" + 
    "v:" + str(int(vers.item()))
  )
  return -dps


##
## @brief      Wrapper for differential evolution
##
## @param      talent_combination  The talent combination to use
##
## @return     Touple (talent_combination, dps, crit, haste, mastery, vers) all as s
##
def differential_evolution_wrapper(args, talent_combination):
  bounds = [
    (0, args.secondaries_amount),
    (0, args.secondaries_amount),
    (0, args.secondaries_amount),
    (0, args.secondaries_amount)
  ]
  arguments = (args, talent_combination)
  #print("  Pos\tTalents\t\tDPS\t\tCrit\tHaste\tMastery\tVersatility")
  ## TODO: Might have to recheck tol here!
  result = differential_evolution(
    __differential_evolution_catcher, 
    bounds, 
    args=arguments, 
    maxiter=15, 
    tol=(float(args.target_error) / 10.0), 
    seed=args.secondaries_amount, 
    disp=True
  )
  crit, haste, mastery, vers = normalize(args, [result.x[0], result.x[1], result.x[2], result.x[3]])
  return (
    talent_combination,
    str(int(-result.fun)),
    str(crit),
    str(haste),
    str(mastery),
    str(vers)
  )
