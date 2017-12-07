# -*- coding: utf-8 -*-
#!python3

import libraries.methods.sim_it as sim_it


def fixed_steps(args, talent_combination):

  crit = int(args.lower_bound_crit)
  haste = int(args.lower_bound_haste)
  mastery = int(args.lower_bound_mastery)
  vers = int(args.lower_bound_versatility)

  step_size = int( args.step_size )

  steps = int(int(args.upper_bound) / step_size)

  # add left over values that are smaller than step size to the base values 631, step_size: 200, relocation of 31 stats
  temp_sum = int( ( ( int( args.upper_bound ) - crit - haste - mastery - vers ) % step_size ) / 4 )
  crit += temp_sum
  haste += temp_sum
  mastery += temp_sum
  vers += temp_sum

  distribution_collection = []

  for c in range(steps + 1):
    for h in range(steps + 1):
      for m in range(steps + 1):
        for v in range(steps + 1):
          # if the sums of each secondary fit the upper_bound
          if crit + c * step_size <= int(args.upper_bound) and haste + h * step_size <= int(args.upper_bound) and mastery + m * step_size <= int(args.upper_bound) and vers + v * step_size <= int(args.upper_bound):
            temp_sum = crit + c * step_size + haste + h * step_size + mastery + m * step_size + vers + v * step_size - int(args.secondaries_amount)
            # if the remaining difference is smaller than the step size, therefore can't be reached using steps
            if temp_sum <= 0 and temp_sum > -step_size:
              # add this distribution to the collection which will be simmed using profilesets later
              # rounded to full int, the loss of 5 rating at max is not relevant
              distribution_collection.append((
                int(crit + c * step_size - temp_sum / 4),
                int(haste + h * step_size - temp_sum / 4),
                int(mastery + m * step_size - temp_sum / 4),
                int(vers + v * step_size - temp_sum / 4)
              ))

  print("Found valid secondary combinations for " + talent_combination + ": " + str(len(distribution_collection)))
  print( "This will take a while without further output. Wait...\r" )
  best_result_dps, best_result_crit, best_result_haste, best_result_mastery, best_result_vers = sim_it.sim_secondaries_profilesets(args, talent_combination, distribution_collection)

  return (
    talent_combination,
    str(best_result_dps),
    str(best_result_crit),
    str(best_result_haste),
    str(best_result_mastery),
    str(best_result_vers)
  )
