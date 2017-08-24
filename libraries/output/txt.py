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

      if all_simmed_values:
        massaged_collection = {}

        for simulation in all_simmed_values[result[0]]:
          not_in_yet = True

          if massaged_collection:
            for massaged_value in massaged_collection[result[0]]:
              if massaged_value[1] == simulation[1] and massaged_value[2] == simulation[2] and massaged_value[3] == simulation[3] and massaged_value[4] == simulation[4]:
                not_in_yet = False
          else:
            massaged_collection[result[0]] = []

          if not_in_yet:
            massaged_collection[result[0]].append(simulation)

        for one_simulation in massaged_collection[result[0]]:
          if ( 100 - (int(one_simulation[0]) * 100 / int(result[1]) ) < 1.0 ):
            file.write("  " + one_simulation[0] + "\t" + one_simulation[1] + "\t" + one_simulation[2] + "\t" + one_simulation[3] + "\t" + one_simulation[4] + "\n")
  return True
      