#!python3

def txt_output(file_name, results):
  with open(file_name + ".txt", "a") as file:
    # TODO: Maybe add simulation values...
    for result in results:
      for value in result:
        file.write(value)
        if value is result[-1]:
          file.write("\n")
        else:
          file.write("\t")
  return True
      