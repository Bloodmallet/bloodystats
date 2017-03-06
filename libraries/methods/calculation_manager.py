#!python3
## Library to manage all available calculation methods

from libraries.methods.differential_evolution import differential_evolution_wrapper


def __get_calculation_methods():
  return (
    "differential_evolution",
  )


def is_calculation_method(method):
  if method in __get_calculation_methods():
    return True
  return False


def calculation_manager(args, talent_combination):
  package = (
    talent_combination,
    "0",
    "0",
    "0",
    "0",
    "0"
  )
  if args.calculation_method == "differential_evolution":
    package = differential_evolution_wrapper(args, talent_combination)
  return package