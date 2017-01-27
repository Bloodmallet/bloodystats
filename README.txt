Introduction and Guidelines

IMPORTANT: Bloodystats calculates either ALL talent combinations you saved in 'custom_talent_combinations.simc' or all talent combinations possible with a two digit number X representing the last two dps-talent-rows for that spec (parameter -t X).


1) Bloodystats is developed using python 3.5. An exe file isn't provided for the time beeing.
	- add a directory 'Bloodystats' inside your <SimulationCraft> directory (however that is called at your system)


2) Usage
	- open the basic Commandline from Windows by Shift+right clicking inside the 'Bloodystats' directory
	- enter 'python bloodystats.py <race> <class> <spec>' without '' and < > to use talent combinations from 'custom_talent_combinations.simc' OR
	- enter 'python bloodystats.py <race> <class> <spec> -t XY' without '' and < > to calculate all talent combinations with Y as the last and X as the second last dps-talent-row-choice. Further examples with actual values can be found in the "Examples" topic.


3) Developer tips
	If you want to test with a different apl or gear than the normal apl file from SImulationCraft provides, just open that file and change whatever you want to change. But make sure:
	a) the outcommented lines at the bottom (summary of your secondary and primary stats) reflect your new equip 
	b) whatever talent combination you want to test: it HAS to be inside 'custom_talent_combinations' or use -t. The talent combination inside the default apl file will be overwritten by Bloodystats.

	For further params please see to 'python bloodystats.py -h' / 'python bloodystats.py --help'


4) Examples
	Everything was tested on Win10 Home 64 Edition, using Windows standard commandline

	'python bloodystats.py orc rogue assassination' - calculates all talent combinations for assassination rogue contained in 'custom_talent_combinations'

	'python bloodystats.py dwarf shaman elemental -t 32 -f 2 -html' - calculates all talent combinations available in combination with the last two dps talent rows where the second last has the right talent and the last has the middle one for LightMovement. Additionally all calculations create and overwrite a html file.

	'python bloodystats.py human mage arcane -t2 -t4' same as first but in addition with the tier 19 set 2 and 4 piece bonus

5) Contact
	Hit me up on Discord: https://discord.gg/tFR2uvK Channel: #Bloodystats
	
	Feedback is highly appreciated!

  Bloodmallet(EU)