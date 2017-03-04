from scipy.optimize import differential_evolution
import libraries.methods.sim_it as sim_it

##
## @brief      Normalizes four values (so their addition results in secondaries_amount)
##
## @param      values  The values
##
## @return     List of four secondary values as strings
##
def normalize(args, values):
  crit, haste, mastery, vers = values
  manipulator = values[0] + values[1] + values[2] + values[3]

  if manipulator == 0.0:
    manipulator == 1.0

  for i in range(0, 4):
    values[i] = values[i] / manipulator

  for i in range(0, 4):
    if values[i] > 2.0 / 3.0:
      overflow = values[i] - 2.0 / 3.0
      fractional_sum = 0.0
      for j in range(0, 4):
        if j != i:
          fractional_sum += values[j]
      for j in range(0, 4):
        if j != i:
          if fractional_sum == 0.0:
            values[j] = 0.0
          else:
            values[j] += overflow * values[j] / fractional_sum
      values[i] = 2.0 / 3.0
  for i in range(0, 4):
    values[i] = str(int(values[i] * args.secondaries_amount))
  return values


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
  crit, haste, mastery, vers = normalize(args, bounds)
  dps = sim_it.sim_dps(args, talent_combination, crit, haste, mastery, vers)
  # TODO: Add and option to hide/show this
  print(str(args.current_combination_count) + "/" + str(args.combination_count) + "\t" + talent_combination + "\t\t" + str(dps) + "\t\t" + str(int(crit.item())) + "\t" + str(int(haste.item())) + "\t" + str(int(mastery.item())) + "\t" + str(int(vers.item())))
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
  print("Pos\tTalents\t\tDPS\t\tCrit\tHaste\tMastery\tVersatility")
  ## TODO: Might have to recheck tol here!
  result = differential_evolution(
    __differential_evolution_catcher, 
    bounds, 
    args=arguments, 
    maxiter=15, 
    tol=(float(args.target_error)), 
    seed=args.secondaries_amount, 
    disp=True
  )
  return (
    talent_combination,
    str(-result.fun),
    str(result.x[0]),
    str(result.x[1]),
    str(result.x[2]),
    str(result.x[3])
  )
