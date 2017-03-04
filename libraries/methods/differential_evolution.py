from scipy.optimize import differential_evolution


##
## @brief      Normalizes four values (so their addition results in secondaries_amount)
##
## @param      values  The values
##
## @return     List of four secondary values as strings
##
def normalize(values):
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
    values[i] = str(int(values[i] * secondaries_amount))
  return values


##
## @brief      Function used by differential evolution to create correct input
##
## @param      bounds              The bounds (crit, haste, mastery, vers)
## @param      talent_combination  The talent combination
##
## @return     negative dps
##
def __differential_evolution_catcher(bounds, *talent_combination):
  crit, haste, mastery, vers = normalize(bounds)
  dps = sim_dps(talent_combination, crit, haste, mastery, vers)
  # TODO: Add and option to hide/show this
  print(str(current_combination_count) + "/" + str(combination_count) + "\t" + talent_combination + "\t" + dps + "\t" + crit + "\t" + haste + "\t" + mastery + "\t" + vers)
  return -float(dps)


##
## @brief      Wrapper for differential evolution
##
## @param      talent_combination  The talent combination to use
##
## @return     Touple (talent_combination, dps, crit, haste, mastery, vers) all as s
##
def differential_evolution_wrapper(talent_combination):
  bounds = [
    (0, secondaries_amount),
    (0, secondaries_amount),
    (0, secondaries_amount),
    (0, secondaries_amount)
  ]
  arguments = (talent_combination)
  ## TODO: Might have to recheck tol here!
  result = differential_evolution(
    __differential_evolution_catcher, 
    bounds, 
    args=arguments, 
    maxiter=15, 
    tol=(double(args.target_error)), 
    seed=secondaries_amount, 
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
