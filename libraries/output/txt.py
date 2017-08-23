#!python3

def txt_output(file_name, results, all_simmed_values={}):
  with open(file_name + ".txt", "a") as file:
    # TODO: Maybe add simulation values...
    for result in results:
      for value in result:
        file.write(value)
        if value is result[-1]:
          file.write("\n")
        else:
          file.write("\t")
        for one_simulation in all_simmed_values[result[0]]:
          file.write("  " + one_simulation[0] + "\t" + one_simulation[1] + "\t" + one_simulation[2] + "\t" + one_simulation[3] + "\t" + one_simulation[4] + "\n")
  return True
      