#!python3
## Library to manage all available calculation methods

from libraries.methods.differential_evolution import differential_evolution_wrapper
from libraries.methods.fixed_steps import fixed_steps


def __get_calculation_methods():
  return (
    "differential_evolution",
    "fixed_steps",
  )


def is_calculation_method(method):
  if method in __get_calculation_methods():
    return True
  return False


def calculation_manager(args, talent_combination):
  package = (
    talent_combination,
    "0", # dps
    "0", # crit
    "0", # haste
    "0", # mastery
    "0"  # versatility
  )
  if args.calculation_method == "differential_evolution":
    package = differential_evolution_wrapper(args, talent_combination)
  elif args.calculation_method == "fixed_steps":
    package = fixed_steps(args, talent_combination)
  return package