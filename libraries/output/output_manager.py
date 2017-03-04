#!python3
#Library to manage ouput of Bloodystats

from libraries.output.txt import txt_output


def __get_ouput():
  return (
    "txt",
  )


def is_output(output):
  if ouput in __get_ouput():
    return True
  return False


def output_manager(results):
  file_name = base_name
  for output in args.output:
    if output == "txt":
      txt_output(file_name, results)
  return True