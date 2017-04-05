#!python3
#Library to manage ouput of Bloodystats

from libraries.output.txt import txt_output


##
## @brief      Gets the output.
##
## @return     The output.
##
def __get_output():
  return (
    "txt",
  )


##
## @brief      Determines if output.
##
## @param      output  The output
##
## @return     True if output, False otherwise.
##
def is_output(output):
  if output in __get_output():
    return True
  return False


##
## @brief      Manages output
##
## @param      args     The arguments
## @param      results  The results
## @param      logging  True if it's alogging entry
##
## @return     True if nothing failed
##
def output_manager(args, results, logging):
  file_name = args.base_name
  for output in args.output:
    if output == "txt":
      if logging:
        txt_output("log", results)
      else:
        txt_output(file_name, results)
  return True