#!python3
#Library to manage ouput of Bloodystats

from libraries.output.txt import txt_output


def __get_output():
  return (
    "txt",
  )


def is_output(output):
  if output in __get_output():
    return True
  return False


def output_manager(args, results):
  file_name = args.base_name
  for output in args.output:
    if output == "txt":
      txt_output(file_name, results)
  return True