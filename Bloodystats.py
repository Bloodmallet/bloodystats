###############################################
#
# Elemental Shaman only
#
# This script uses SimulationCraft to get the
# best secondary stat distribution for a given
# talent combination.
#
# Read README.txt to install correctly
#
# Script is written on and for Windows 10 only.
#
# This program is provided as is. No warranity
# of any kind is given. Use it at your own risk.
#
# TORESEARCH: item budget depending on iLevel,
#	to determine secondary stat pool and primary
#
# TODO:
#		param for one single talent combination
#		tanks?
# How to build:
# 	use powershell and 
# 	pyinstaller .\Bloodystats.spec
#
#
# Questions, ideas? Hit me up on Discord:
# https://discord.gg/tFR2uvK
# Channel: #Bloodystats
#								BloodmalletEU
##############################################


#-------------------
# Import
#-------------------

# Library to use command line
import subprocess
# Library to get date and calcutiontime for program
import datetime
# Library to look for files and create them if needed
import os
# params
import argparse
# differential evolution...
from scipy.optimize import differential_evolution


#-----------------
# Argument parser
#-----------------

parser = argparse.ArgumentParser(description="Program from BloodmalletEU. Base idea from Binkenstein. Questions, ideas? Hit me up on Discord: https://discord.me/earthshrine #bloodystats -Program calculates best secondary stat distribution for talent combinations. Version:29.08.16")
parser.add_argument("race_choice", nargs="?", default="dwarf", choices=["dwarf", "gnome", "human", "draenei", "nightelf", "worgen", "pandaren", "orc", "troll", "tauren", "undead", "bloodelf", "goblin"], help="Name of the race")
parser.add_argument("class_choice", nargs="?", default="shaman", choices=["death_knight", "paladin", "shaman", "hunter", "rogue", "warrior", "demon_hunter", "mage", "warlock", "monk", "druid", "priest"], help="Name of the class of your character")
parser.add_argument("spec_choice", nargs="?", default="elemental", help="Name of the specialisation of your character")
parser.add_argument("-f", "--fight_type", dest="fight_choosen", nargs="?", default="1", choices=["-1", "1", "2", "3", "4", "5"], help="Default: -1; Choose one of six: <1>Patchwerk, <2>LightMovement, <3>HeavyMovement, <4>Darmac, <5>Helter Skelter, <-1> enables custom_fight_style.simc")
parser.add_argument("-t", "--talent_combination", dest="talent_choosen", nargs="?", default="-1", choices=["-1", "11", "12", "13", "21", "22", "23", "31", "32", "33"], help="Talentselection of the last two rows. E.g. (12) or (33). (-1) enables custom_talent_combinations.simc")
# simc target_error=(0.5 /accuracy) and DE tol=(0.5*3/100 / accuracy)
parser.add_argument("-a", "--accuracy", dest="accuracy", nargs="?", default=10, type=int, help="Default: 10; Increase to increase accuracy of default calculation. Not recommended")
parser.add_argument("-cs", "--character_stats", action="store_const", const=True, default=False, help="Enables character_stats.simc")
parser.add_argument("-t2", "--tier_set_bonus2", dest="t2", action="store_const", const=True, default=False, help="Enable T19-2 piece bonus.")
parser.add_argument("-t4", "--tier_set_bonus4", dest="t4", action="store_const", const=True, default=False, help="Enable T19-4 piece bonus.")
parser.add_argument("-html", action="store_const", const=True, default=False, help="Enable html output for simulationcraft. (Spam your disk w00p w00p!)" )
parser.add_argument("-threads", nargs="?", default="", help="Default: max; Provide a number to determine how many threads to use.")
parser.add_argument("-se", "--silent_end", dest="silent_end", action="store_const", const=True, default=False, help="Let the program terminate without user input. You wont be able to see how long it took.")
parser.add_argument("-grad", "--gradient_calculation", dest="calculation_type", action="store_const", const="1", default="0", help="Give this option to use gradient calculation to determine best secondary stat distribution. May not find the global maximum but local. Could be faster.")
parser.add_argument("-+grad", "--additional_grad", dest="additional_grad", action="store_const", const=True, default=False, help="Add this to DE to finalize values with a gradient function. Handy for lower -a")
parser.add_argument("--delta", dest="deltaValue", nargs="?", default=100, type=int, help="Default: 100; Determines the stepsize of the gradient method (-+grad)")
parser.add_argument("--tier_number", dest="tier_number", nargs="?", default="19", choices=["19"], help="Determine which basic profile will be used for calculations.")
parser.add_argument("--tier_difficulty", dest="tier_difficulty", nargs="?", default="M", choices=["P", "H", "M", "M_NH"], help="Determine which basic profile will be used for calculations.")


args = parser.parse_args()

#-------------------
# Functions
#-------------------
relativePath = ".\\"
# is going to contain all other documents...currently not!
# filedictionary = {"character_stats.simc": ''' MISSING! GET IT FROM ZIP ''', "custom_fight_style.simc": ''' MISSING! GET IT FROM ZIP ''', "custom_talent_combinations.simc": ''' MISSING! GET IT FROM ZIP '''}
classdictionary = {	"shaman": 		{"talents": "1001111", "specs": ("elemental", "enhancement")				},
					"mage": 		{"talents": "1011011", "specs": ("fire", "frost", "arcane")					},
					"druid": 		{"talents": "1000111", "specs": ("balance", "feral")						},
					"priest": 		{"talents": "1001111", "specs": ("shadow")									},
					"warlock": 		{"talents": "1101011", "specs": ("affliction", "destruction", "demonology")	},
					"hunter": 		{"talents": "1101011", "specs": ("mm", "sv", "bm")							},
					"death_knight":	{"talents": "1110011", "specs": ("unholy", "frost")							},
					"demon_hunter":	{"talents": "1110111", "specs": ("havoc")									},
					"monk": 		{"talents": "1010011", "specs": ("windwalker")								},
					"paladin": 		{"talents": "1101001", "specs": ("retribution")								},
					"rogue": 		{"talents": "1110111", "specs": ("assassination", "sublety", "outlaw")		},
					"warrior": 		{"talents": "1010111", "specs": ("arms", "fury")							}}

def checkTalent(talent_combination):
	for i in range(0, 7):
		if classdictionary[args.class_choice]["talents"][i] == "0" and talent_combination[i] != "0":
			return False
		if classdictionary[args.class_choice]["talents"][i] == "1" and talent_combination[i] == "0":
			return False
	last = True
	previous = False
	for i in range(0, 7):
		if last and classdictionary[args.class_choice]["talents"][6-i] == "1":
			if args.talent_choosen[1] != talent_combination[6-i]:
				return False
			last = False
			previous = True
		elif previous and classdictionary[args.class_choice]["talents"][6-i] == "1":
			if args.talent_choosen[0] != talent_combination[6-i]:
				return False
			previous = False
	return True

# TODO: Include again?
# def checkForFile(filename):
# 	if os.path.isdir(relativePath):
# 		if os.path.isfile(relativePath + filename):
# 			return True
# 	return False
# 
# def createFile(filename):
# 	if not os.path.exists(relativePath):
# 		os.makedirs(relativePath)
# 	currentfile = open(relativePath + filename, "x")
# 	currentfile.close()
# 	currentfile = open(relativePath + filename, "w")
# 	currentfile.write(filedictionary[filename])
# 	currentfile.close()

def getValue(string):
	# Function to get the float value out of one part of the scale row. Example: haste=6.43(0.14)
    return float(string.split("=")[1].split("(")[0])

def gradient_func(secondary_values, stuff):
	# stuff contains: talent_selection, globPos
	# stat distribution to start the gradient function
	gear_crit_rating = secondary_values["crit"]
	gear_haste_rating = secondary_values["haste"]
	gear_mastery_rating = secondary_values["mastery"]
	gear_versatility_rating = secondary_values["vers"]

	searchInProgress = True
	iteration = 0
	max_iteration_counter = int(basic_secondary_stats_amount / args.deltaValue) / 2
	errormargin = 0.05
	if args.additional_grad:
		errormargin = 0.1
		max_iteration_counter = int(basic_secondary_stats_amount / args.deltaValue) / 4
	while iteration < max_iteration_counter and searchInProgress:
		argument = relativePath + "..\\simc.exe "
		argument += char_values + " "
		argument += "iterations=10000 "
		argument += "target_error=0.0 "
		argument += "threads=" + args.threads + " "
		if args.html:
			argument += "html=" + dateOfSimulation + "_scaling_of_" + args.race_choice + "_" + args.spec_choice + "_" + fight_style + "_" + stuff["talent_selection"]
			if args.fight_choosen == "-1":
				argument += "_customFight"
			argument += ".html "
		if fight_style == "custom":
			argument += "custom_fight_style.simc "
		else:
			argument += "fight_style=" + fight_style + " "
		argument += "race=" + args.race_choice + " "
		#argument += args.class_choice + "=Bloodystats "
		#argument += "spec=" + args.spec_choice + " "
		argument += "calculate_scale_factors=1 "
		argument += "scale_only=crit,haste,mastery,versatility "
		argument += "scale_strength=320 "
		#argument += "name=" + nameOfSimulation + " "
		argument += "talents=" + stuff["talent_selection"] + " "
		#argument += "apl.simc "
		if args.character_stats:
			argument += "character_stats.simc "
		argument += gear_mainstat + " "
		argument += "gear_crit_rating=" + str(gear_crit_rating) + " "
		argument += "gear_haste_rating=" + str(gear_haste_rating) + " "
		argument += "gear_mastery_rating=" + str(gear_mastery_rating) + " "
		argument += "gear_versatility_rating=" + str(gear_versatility_rating) + " "
		if args.t2:
			argument += "set_bonus=tier19_2pc=1 "
		if args.t4:
			argument += "set_bonus=tier19_4pc=1 "

		# Simulating
		#print(argument)
		whole_sim = subprocess.run(argument, stdout=subprocess.PIPE, universal_newlines=True)
		# Catching result and getting values out of it
		owndps = True
		ownweights = True
		simdps = "0"
		for line in whole_sim.stdout.splitlines():
			if "Weights :" in line and ownweights:
				scaling = line
				ownweights = False
			if "DPS:" in line and owndps:
				simdps = line
				owndps = False
		print("global " + stuff["globPos"] + " DPS: " + simdps.split()[1] + " | ", end="")

		# gotten_Int = getValue(scaling.split()[1])
		gotten_crit = getValue(scaling.split()[4])
		gotten_haste = getValue(scaling.split()[5])
		gotten_mastery = getValue(scaling.split()[6])
		gotten_vers = getValue(scaling.split()[7])
		
		# highest element gets points, lowest element loses them; I wish I'd know how to automate this part...
		# probably with some kind of dictionary? {"highest": "", "lowest": ""} and another one with the values?
		# works fine but would need the same bloated part here
		if gotten_crit >= gotten_haste and gotten_crit >= gotten_mastery and gotten_crit >= gotten_vers:
			if gotten_haste <= gotten_mastery and gotten_haste <= gotten_vers:
				if gotten_crit - gotten_haste <= errormargin:
					print("Values are nearly equal. Ending process")
					searchInProgress = False
				elif gear_haste_rating >= args.deltaValue:
					gear_haste_rating = gear_haste_rating - args.deltaValue
					gear_crit_rating = gear_crit_rating + args.deltaValue
					print("+ Crit (" + str(gotten_crit) + ") | - Haste (" + str(gotten_haste) + ")")
				else:
					searchInProgress = False
			elif gotten_mastery <= gotten_haste and gotten_mastery <= gotten_vers:
				if gotten_crit - gotten_mastery <= errormargin:
					print("Values are nearly equal. Ending process")
					searchInProgress = False
				elif gear_mastery_rating >= args.deltaValue:
					gear_mastery_rating = gear_mastery_rating - args.deltaValue
					gear_crit_rating = gear_crit_rating + args.deltaValue
					print("+ Crit (" + str(gotten_crit) + ") | - Mastery (" + str(gotten_mastery) + ")")
				else:
					searchInProgress = False
			elif gotten_vers <= gotten_haste and gotten_vers <= gotten_mastery:
				if gotten_crit - gotten_vers <= errormargin:
					print("Values are nearly equal. Ending process")
					searchInProgress = False
				elif gear_versatility_rating >= args.deltaValue:
					gear_versatility_rating = gear_versatility_rating - args.deltaValue
					gear_crit_rating = gear_crit_rating + args.deltaValue
					print("+ Crit (" + str(gotten_crit) + ") | - Versatility (" + str(gotten_vers) + ")")
				else:
					searchInProgress = False
		elif gotten_haste >= gotten_crit and gotten_haste >= gotten_mastery and gotten_haste >= gotten_vers:
			if gotten_crit <= gotten_mastery and gotten_crit <= gotten_vers:
				if gotten_haste - gotten_crit <= errormargin:
					print("Values are nearly equal. Ending process")
					searchInProgress = False
				elif gear_crit_rating >= args.deltaValue:
					gear_crit_rating = gear_crit_rating - args.deltaValue
					gear_haste_rating = gear_haste_rating + args.deltaValue
					print("+ Haste (" + str(gotten_haste) + ") | - Crit (" + str(gotten_crit) + ")")
				else:
					searchInProgress=False
			elif gotten_mastery <= gotten_crit and gotten_mastery <= gotten_vers:
				if gotten_haste - gotten_mastery <= errormargin:
					print("Values are nearly equal. Ending process")
					searchInProgress = False
				elif gear_mastery_rating >= args.deltaValue:
					gear_mastery_rating = gear_mastery_rating - args.deltaValue
					gear_haste_rating = gear_haste_rating + args.deltaValue
					print("+ Haste (" + str(gotten_haste) + ") | - Mastery (" + str(gotten_mastery) + ")")
				else:
					searchInProgress=False
			elif gotten_vers <= gotten_crit and gotten_vers <= gotten_mastery:
				if gotten_haste - gotten_vers <= errormargin:
					print("Values are nearly equal. Ending process")
					searchInProgress = False
				elif gear_versatility_rating >= args.deltaValue:
					gear_versatility_rating = gear_versatility_rating - args.deltaValue
					gear_haste_rating = gear_haste_rating + args.deltaValue
					print("+ Haste (" + str(gotten_haste) + ") | - Versatility (" + str(gotten_vers) + ")")
				else:
					searchInProgress=False
		elif gotten_mastery >= gotten_crit and gotten_mastery >= gotten_haste and gotten_mastery >= gotten_vers:
			if gotten_crit <= gotten_haste and gotten_crit <= gotten_vers:
				if gotten_mastery - gotten_crit <= errormargin:
					print("Values are nearly equal. Ending process")
					searchInProgress = False
				elif gear_crit_rating >= args.deltaValue:
					gear_crit_rating = gear_crit_rating - args.deltaValue
					gear_mastery_rating = gear_mastery_rating + args.deltaValue
					print("+ Mastery (" + str(gotten_mastery) + ") | - Crit (" + str(gotten_crit) + ")")
				else:
					searchInProgress=False
			elif gotten_haste <= gotten_crit and gotten_haste <= gotten_vers:
				if gotten_mastery - gotten_haste <= errormargin:
					print("Values are nearly equal. Ending process")
					searchInProgress = False
				elif gear_haste_rating >= args.deltaValue:
					gear_haste_rating = gear_haste_rating - args.deltaValue
					gear_mastery_rating = gear_mastery_rating + args.deltaValue
					print("+ Mastery (" + str(gotten_mastery) + ") | - Haste (" + str(gotten_haste) + ")")
				else:
					searchInProgress=False
			elif gotten_vers <= gotten_crit and gotten_vers <= gotten_haste:
				if gotten_mastery - gotten_vers <= errormargin:
					print("Values are nearly equal. Ending process")
					searchInProgress = False
				elif gear_versatility_rating >= args.deltaValue:
					gear_versatility_rating = gear_versatility_rating - args.deltaValue
					gear_mastery_rating = gear_mastery_rating + args.deltaValue
					print("+ Mastery (" + str(gotten_mastery) + ") | - Versatility (" + str(gotten_vers) + ")")
				else:
					searchInProgress=False
		elif gotten_vers >= gotten_crit and gotten_vers >= gotten_haste and gotten_vers >= gotten_mastery:
			if gotten_crit <= gotten_haste and gotten_crit <= gotten_mastery:
				if gotten_vers - gotten_crit <= errormargin:
					print("Values are nearly equal. Ending process")
					searchInProgress = False
				elif gear_crit_rating >= args.deltaValue:
					gear_crit_rating = gear_crit_rating - args.deltaValue
					gear_versatility_rating = gear_versatility_rating + args.deltaValue
					print("+ Versatility (" + str(gotten_vers) + ") | - Crit (" + str(gotten_crit) + ")")
				else:
					searchInProgress=False
			elif gotten_haste <= gotten_crit and gotten_haste <= gotten_mastery:
				if gotten_vers - gotten_haste <= errormargin:
					print("Values are nearly equal. Ending process")
					searchInProgress = False
				elif gear_haste_rating >= args.deltaValue:
					gear_haste_rating = gear_haste_rating - args.deltaValue
					gear_versatility_rating = gear_versatility_rating + args.deltaValue
					print("+ Versatility (" + str(gotten_vers) + ") | - Haste (" + str(gotten_haste) + ")")
				else:
					searchInProgress=False
			elif gotten_mastery <= gotten_crit and gotten_mastery <= gotten_haste:
				if gotten_vers - gotten_mastery <= errormargin:
					print("Values are nearly equal. Ending process")
					searchInProgress = False
				elif gear_mastery_rating >= args.deltaValue:
					gear_mastery_rating = gear_mastery_rating - args.deltaValue
					gear_versatility_rating = gear_versatility_rating + args.deltaValue
					print("+ Versatility (" + str(gotten_vers) + ") | - Mastery (" + str(gotten_mastery) + ")")
				else:
					searchInProgress=False
		iteration = iteration + 1
	# returns talent_selection, dps, crit, haste, mastery, vers
	result = {"talent_selection": simulation_dictionary["talent_selection"], "dps": simdps.split()[1], "crit": gear_crit_rating, "haste": gear_haste_rating, "mastery": gear_mastery_rating, "vers": gear_versatility_rating}
	return result

##
# differential evolution (de)
# function whis is called and uses simc
def de_func(values, *stuff):
	crit_factor, haste_factor, mastery_factor, vers_factor = values

	manipulator = crit_factor + haste_factor + mastery_factor + vers_factor
	if manipulator == 0.0:
		manipulator = 1.0
	# normalising values
	crit_factor = crit_factor / manipulator
	haste_factor = haste_factor / manipulator
	mastery_factor = mastery_factor / manipulator
	vers_factor = vers_factor / manipulator


	# force each value to max of 2/3.
	factor_heap = [crit_factor, haste_factor, mastery_factor, vers_factor]

	for v in range(0, 4):
		if factor_heap[v] > 2/3:
			overflow = factor_heap[v] - 2 / 3
			partial_sum = 0.0
			for t in range(0, 4):
				if factor_heap[t] != factor_heap[v]:
					partial_sum = partial_sum + factor_heap[t]
			for t in range(0, 4):
				if t != v:
					if partial_sum == 0.0:
						factor_heap[t] = 1 / 9
					else:
						factor_heap[t] = factor_heap[t] + overflow * factor_heap[t] / partial_sum
			factor_heap[v] = 2 / 3

	crit_factor = factor_heap[0]
	haste_factor = factor_heap[1]
	mastery_factor = factor_heap[2]
	vers_factor = factor_heap[3]

	crit = int(crit_factor * basic_secondary_stats_amount)
	haste = int(haste_factor * basic_secondary_stats_amount)
	mastery = int(mastery_factor * basic_secondary_stats_amount)
	vers = int(vers_factor * basic_secondary_stats_amount)

	# get other important values
	talent_selection, globPos = stuff

	argument = relativePath + "..\\simc.exe "
	argument += char_values + " "
	argument += "iterations=50000 "
	argument += "target_error=" + str(base_accuracy / args.accuracy) + " " 
	argument += "threads=" + args.threads + " "
	if args.html:
		argument += "html=" + dateOfSimulation + "_scaling_of_" + args.race_choice + "_" + args.spec_choice + "_" + fight_style + "_" + talent_selection
		if args.fight_choosen == "-1":
			argument += "_customFight"
		argument += ".html "
	if fight_style == "custom":
		argument += "custom_fight_style.simc "
	else:
		argument += "fight_style=" + fight_style + " "
	argument += "race=" + args.race_choice + " "
	argument += "talents=" + talent_selection + " "
	if args.character_stats:
		argument += "character_stats.simc "
	argument += "calculate_scale_factors=0 "
	argument += gear_mainstat + " "
	argument += "gear_crit_rating=" + str(crit) + " "
	argument += "gear_haste_rating=" + str(haste) + " "
	argument += "gear_mastery_rating=" + str(mastery) + " "
	argument += "gear_versatility_rating=" + str(vers) + " "
	if args.t2:
		argument += "set_bonus=tier19_2pc=1 "
	if args.t4:
		argument += "set_bonus=tier19_4pc=1 "

	# Simulating
	#print(argument)
	whole_sim = subprocess.run(argument, stdout=subprocess.PIPE, universal_newlines=True)
	# Catching result and getting values out of it
	owndps = True
	simdps = "0"
	for line in whole_sim.stdout.splitlines():
		if "DPS:" in line:
			if owndps:
				simdps = line
				owndps = False
	# TODO: Decide to hide this
	#print(".", end="")
	print("global " + globPos + " DPS:\t" + simdps.split()[1] + "\t" + str(crit) + "\t" + str(haste) + "\t" + str(mastery) + "\t" + str(vers))
	return -float(simdps.split()[1])

##
# function which starts the differential evolution
# dictionary contains talent_selection and globPos
def de_call(dictionary):
	print("Don't worry, be happy. DE Call for " + dictionary["talent_selection"])
	#twothird = 2 / 3 * basic_secondary_stats_amount
	#bounds = [(0, twothird), (0, twothird), (0, twothird), (0, twothird)]
	print("Following lines:\tDPS\t\tcrit\thaste\tmastery\tversatility")
	bounds = [(0, basic_secondary_stats_amount), (0, basic_secondary_stats_amount), (0, basic_secondary_stats_amount), (0, basic_secondary_stats_amount)]
	arguments = (dictionary["talent_selection"], dictionary["globPos"])
	# DE!
	result = differential_evolution(de_func, bounds, args=arguments, maxiter=15, tol=(base_accuracy * 3 / 100 / args.accuracy), polish=True, seed=basic_secondary_stats_amount, disp=True)
	# TODO: Decide to hide this
	#print(result)
	normalizor = result.x[0] + result.x[1] + result.x[2] + result.x[3]
	package = {"talent_selection": simulation_dictionary["talent_selection"], "dps": str(-result.fun), "crit": int(result.x[0] * basic_secondary_stats_amount / normalizor), "haste": int(result.x[1] * basic_secondary_stats_amount / normalizor), "mastery": int(result.x[2] * basic_secondary_stats_amount / normalizor), "vers": int(result.x[3] * basic_secondary_stats_amount / normalizor)}
	print(package)
	if args.additional_grad:
		print("Polishing values. Using gradient method")
		result_GRAD = gradient_func(package, dictionary)
		return result_GRAD
	else:
		return package

# global check for validity of input
if args.class_choice in classdictionary and args.spec_choice in classdictionary[args.class_choice]["specs"]:

	#-------------------
	# Default values
	# overwritten by user input and .simc files
	#-------------------

	fight_style = "patchwerk"

	char_values = relativePath + "..\\profiles\\Tier" + args.tier_number + args.tier_difficulty + "\\" + args.class_choice + "_" + args.spec_choice + "_T" + args.tier_number + args.tier_difficulty + ".simc"

	# used for target_error of simc and tol of DE
	base_accuracy = 0.5
	# change per evaluation

	# stats
	basic_secondary_stats_amount = 4
	gear_mainstat = "1"
	#gear_intellect = 22000
	#gear_strength = 22000
	#gear_agility = 22000
	gear_crit_rating = basic_secondary_stats_amount / 4
	gear_haste_rating = basic_secondary_stats_amount / 4
	gear_mastery_rating = basic_secondary_stats_amount / 4
	gear_versatility_rating = basic_secondary_stats_amount / 4

	# talent combination one wants to test
	#talent_selection = "0000000"

	#-------------------------------------------------------
	#
	# Scaning for Files, generating them if nonexistent
	# if there: getting values
	#
	#-------------------------------------------------------

	# TODO: include again?
	# print("Scanning for required files.")
	# for filename in sorted(filedictionary.keys()):
	# 	print("Checking " + filename + ".....", end=""),
	# 	if checkForFile(filename):
	# 		print("OK")
	# 	else:
	# 		print("Missing")
	# 		print("Creating " + filename + ".....", end="")
	# 		createFile(filename)
	# 		print("Done")
	# print("Scanning complete.")
	# print("------------------------")
	print("Grabbing default values.")
	# Getting Stats from templates
	with open(char_values, "r") as character_stats:
		for line in character_stats:
			if "gear_intellect=" in line:
				if int(line.split("=")[1]) > 0:
					while line[0] != "g":
						line = line[1:]
					if line[-1] == "\n":
						gear_mainstat = line[:-1]
					else:
						gear_mainstat = line
					print("Grabbed mainstat:" + gear_mainstat)
			elif "gear_strength=" in line:
				if int(line.split("=")[1]) > 0:
					while line[0] != "g":
						line = line[1:]
					if line[-1] == "\n":
						gear_mainstat = line[:-1]
					else:
						gear_mainstat = line
					print("Grabbed mainstat:" + gear_mainstat)
			elif "gear_agility=" in line:
				if int(line.split("=")[1]) > 0:
					while line[0] != "g":
						line = line[1:]
					if line[-1] == "\n":
						gear_mainstat = line[:-1]
					else:
						gear_mainstat = line
					print("Grabbed mainstat:" + gear_mainstat)
			elif "gear_crit_rating=" in line:
				gear_crit_rating = line.split("=")[1][:-1]
				print("Grabbed crit: " + gear_crit_rating)
			elif "gear_haste_rating=" in line:
				gear_haste_rating = line.split("=")[1][:-1]
				print("Grabbed haste: " + gear_haste_rating)
			elif "gear_mastery_rating=" in line:
				gear_mastery_rating = line.split("=")[1][:-1]
				print("Grabbed mastery: " + gear_mastery_rating)
			elif "gear_versatility_rating=" in line:
				gear_versatility_rating = line.split("=")[1][:-1]
				print("Grabbed versatility: " + gear_versatility_rating)
	if args.character_stats:
		print("Trying to grab character_stats.simc input")
		with open("character_stats.simc", "r") as character_stats:
			for line in character_stats:
				if "gear_intellect=" in line:
					if int(line.split("=")[1]) > 0:
						while line[0] != "g":
							line = line[1:]
						if line[-1] == "\n":
							gear_mainstat = line[:-1]
						else:
							gear_mainstat = line
						print("Grabbed mainstat:" + gear_mainstat)
				elif "gear_strength=" in line:
					if int(line.split("=")[1]) > 0:
						while line[0] != "g":
							line = line[1:]
						if line[-1] == "\n":
							gear_mainstat = line[:-1]
						else:
							gear_mainstat = line
						print("Grabbed mainstat:" + gear_mainstat)
				elif "gear_agility=" in line:
					if int(line.split("=")[1]) > 0:
						while line[0] != "g":
							line = line[1:]
						if line[-1] == "\n":
							gear_mainstat = line[:-1]
						else:
							gear_mainstat = line
						print("Grabbed mainstat:" + gear_mainstat)
				elif "gear_crit_rating=" in line:
					gear_crit_rating = line.split("=")[1][:-1]
					print("Grabbed crit: " + gear_crit_rating)
				elif "gear_haste_rating=" in line:
					gear_haste_rating = line.split("=")[1][:-1]
					print("Grabbed haste: " + gear_haste_rating)
				elif "gear_mastery_rating=" in line:
					gear_mastery_rating = line.split("=")[1][:-1]
					print("Grabbed mastery: " + gear_mastery_rating)
				elif "gear_versatility_rating=" in line:
					gear_versatility_rating = line.split("=")[1][:-1]
					print("Grabbed versatility: " + gear_versatility_rating)
	basic_secondary_stats_amount = int(gear_crit_rating) + int(gear_versatility_rating) + int(gear_haste_rating) + int(gear_mastery_rating)
	print("Grabbed secondary stat amount: " + str(basic_secondary_stats_amount))
	print("------------------------------")
	print("")
	print("Functionality ensured.")
	#print("This is BloodmalletEU and you're using my addition to SimulationCraft.")
	#print("You're about to calculate stat distributions.")
	#
	##----------------------------------------------------------------------
	##
	## User Interface (not used but printed if provided with enough params)
	##
	##----------------------------------------------------------------------
	#
	#print("")
	#print("Choose your fight style")
	#print("<-1> Custom fight. Go crazy creating that in custom_fight_style.simc")
	#print("<1> Patchwerk (standing still and dealing dps)")
	#print("<2> LightMovement (...self-explanatory)")
	#print("<3> HeavyMovement (...self-explanatory)")
	#print("<4> Beastlord (Movement, frequent Adds spawn and spread Dot)")
	#print("<5> HelterSkelter (shit just got real-notreal, everything is happening)")
	#if args.fight_choosen != "-1":
	#	print("Pre-selected: " + args.fight_choosen)
	#	fight_choice = args.fight_choosen
	#else:
	#	fight_choice = input("Number of fight style without < and >: ")
	if args.fight_choosen == "-1":
		fight_style = "custom"
	elif args.fight_choosen == "1":
		fight_style = "Patchwerk"
	elif args.fight_choosen == "2":
		fight_style = "LightMovement"
	elif args.fight_choosen == "3":
		fight_style = "HeavyMovement"
	elif args.fight_choosen == "4":
		fight_style = "Beastlord"
	elif args.fight_choosen == "5":
		fight_style = "HelterSkelter"
	#print("")
	#print("Talent combination should be provided as 11, 12, 13, 21 up to 33 representing the chosen talents in the last two dps rows. Every possible talentcombination with your inserted one except for the utility tiers will be calculated. Beware the calculation time...")
	#
	if args.talent_choosen == "-1":
		print("Talent combinations will be read from file.")
	#elif args.talent_choosen != "-1":
	#	print("Pre-selected: " + args.talent_choosen)
	#	talent_choice = args.talent_choosen
	#else:
	#	talent_choice = input("Talent combination of the last two dps tiers or -1 to read from custom_talent_combinations.simc: ")
	#	if talent_choice == "-1":
	#		args.custom_talent_combinations = True
	#
	#-------------------------------------------------------------------
	#
	# Simulations
	# have to switch acconding to talent_combinations (-tc option)
	# between: a) simulating all given talent combinations 
	#          b) normal sim for two predefined talent tiers
	#
	#-------------------------------------------------------------------

	print("Starting calculation of best secondary stat distribution.")
	print("Race: " + args.race_choice)
	print("Specialisation: " + args.spec_choice)
	if args.calculation_type != "0":
		print("Delta: " + str(args.deltaValue))
	print("Amount of secondary stats: " + str(basic_secondary_stats_amount))
	print("Fight type: " + fight_style)

	simulation_start_time = datetime.datetime.now()
	dateOfSimulation = "{:%Y_%m_%d}".format(datetime.datetime.now())
	nameOfSimulation = dateOfSimulation + "_scaling_of_" + args.race_choice + "_" + args.spec_choice + "_" + fight_style
	if args.talent_choosen != "-1":
		nameOfSimulation += "_" + args.talent_choosen
	if args.fight_choosen == "-1":
		nameOfSimulation += "_customFight"

	print("Ready. Set. Go!")
	# start of calculation

	# switch between a and b
	# a here
	if args.talent_choosen == "-1":
		with open(relativePath + "custom_talent_combinations.simc", "r") as f:
			maxCount = sum(1 for _ in f)
		if maxCount == 0:
			print("No talent combination in 'custom_talent_combinations.simc' found. Please add some or use '-t X'.")
		run = 1
		with open(relativePath + "custom_talent_combinations.simc", "r") as talent_heap:
			for line in talent_heap:
				# build simulation_dictionary
				# dictionary: basic_secondary_stats_amount, talent_selection, globPos
				if line[-1:] == "\n":
					simulation_dictionary = {"talent_selection": line[:-1], "globPos": str(run) + "/" + str(maxCount)}
				else:
					simulation_dictionary = {"talent_selection": line, "globPos": str(run) + "/" + str(maxCount)}

				if args.calculation_type == "0":
					distr_knowledge = de_call(simulation_dictionary)
				else:
					gearstats = {"crit": int(basic_secondary_stats_amount/4), "haste": int(basic_secondary_stats_amount/4), "mastery": int(basic_secondary_stats_amount/4), "vers": int(basic_secondary_stats_amount/4)}
					distr_knowledge = gradient_func(gearstats, simulation_dictionary)
				
				# write result to console and file
				print("")
				print("Calculating stat distribution.....Done")
				print("Final secondary stat distribution for " + distr_knowledge["talent_selection"] + " was")
				print("Crit:" + str(distr_knowledge["crit"]))
				print("Haste:" + str(distr_knowledge["haste"]))
				print("Mastery:" + str(distr_knowledge["mastery"]))
				print("Versatility:" + str(distr_knowledge["vers"]))
				with open(dateOfSimulation + "_" + args.race_choice + "_" + args.class_choice + "_" + args.spec_choice + "_" + fight_style + "_customTalentCombinations.txt", "a") as destination:
					destination.write(distr_knowledge["talent_selection"] + "\t")
					destination.write(distr_knowledge["dps"] + "\t")
					destination.write(str(distr_knowledge["crit"]) + "\t")
					destination.write(str(distr_knowledge["haste"]) + "\t")
					destination.write(str(distr_knowledge["mastery"]) + "\t")
					destination.write(str(distr_knowledge["vers"]) + "\n")
				print("Written to file")
				run = run + 1
	else: 
		simulation_number = 1
		for row1 in range(0,4):
			for row2 in range(0,4):
				for row3 in range(0,4):
					for row4 in range(0,4):
						for row5 in range(0,4):
							for row6 in range(0,4):
								for row7 in range(0,4):
									talent_selection = str(row1) + str(row2) + str(row3) + str(row4) + str(row5) + str(row6) + str(row7)
									if checkTalent(talent_selection):
										count_1 = 0
										for i in range(0,7):
											if talent_selection[i] != "0":
												count_1 = count_1 + 1
										count_1 = count_1 - 2
										simulation_dictionary = {"talent_selection": talent_selection, "globPos": str(simulation_number) + "/" + str(3**count_1)}
										simulation_number = simulation_number + 1
										print("")
										print("Optimizing " + simulation_dictionary["talent_selection"] + " " + simulation_dictionary["globPos"] + ":")
										
										if args.calculation_type == "0":
											distr_knowledge = de_call(simulation_dictionary)
										else:
											gearstats = {"crit": basic_secondary_stats_amount/4, "haste": basic_secondary_stats_amount/4, "mastery": basic_secondary_stats_amount/4, "vers": basic_secondary_stats_amount/4}
											distr_knowledge = gradient_func(gearstats, simulation_dictionary)

										print("")
										print("Calculating stat distribution.....Done")
										print("Final secondary stat distribution for " + distr_knowledge["talent_selection"] + " was")
										print("Crit:" + str(distr_knowledge["crit"]))
										print("Haste:" + str(distr_knowledge["haste"]))
										print("Mastery:" + str(distr_knowledge["mastery"]))
										print("Versatility:" + str(distr_knowledge["vers"]))
										with open(dateOfSimulation + "_" + args.race_choice + "_" + args.class_choice + "_" + args.spec_choice + "_" + fight_style + "_" + args.talent_choosen + ".txt", "a") as destination:
											destination.write(distr_knowledge["talent_selection"] + "\t")
											destination.write(distr_knowledge["dps"] + "\t")
											destination.write(str(distr_knowledge["crit"]) + "\t")
											destination.write(str(distr_knowledge["haste"]) + "\t")
											destination.write(str(distr_knowledge["mastery"]) + "\t")
											destination.write(str(distr_knowledge["vers"]) + "\n")
										print("Written to file")

	# all simulations are done
	simulation_end_time = datetime.datetime.now()
	print("The calculation took " + str(simulation_end_time - simulation_start_time))
	print("\t\twritten by BloodmalletEU")
	if not args.silent_end:
		endsign = input("Press Enter to terminate...")
		print("Aber nu is wirklich Schluss... -_-")

	# simc.exe Bloodystats/simulation_options.simc desired_targets=3 html=simulations/BS.html Bloodystats/character_options.simc calculate_scale_factors=0 scale_only=int,crit,haste,mastery,versatility name=PoF_AS_EF_AfS_LR talents=1002132 Bloodystats/apl.simc Bloodystats/character_stats.simc
# end of global validity check
else:
	print("Your input was invalid. Check out your class + spec choice")