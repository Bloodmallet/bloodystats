Greetings,
I'm Bloodmallet(EU). General support can be found at https://discord.gg/tFR2uvK in #bloodytools. In addition to this you can easily open issues in the repo https://github.com/Bloodmallet/bloodystats/issues .


Content
1) What it does
2) Requirements
3) Setup
4) Examples
5) Talent combinations
6) End


1) What it does
Bloodystats uses SimulationCraft to reseach different secondary stat rating distributions to find the best dps values. It's designed in a way that should make it easy to add different approaches to this problem. Bloodystats has the same limitations / possibilities as SimulationCraft. So you can freely choose a class and spec, a fight style, or define your own, choose a talent combination or multiple. How to? Keep reading.


2) Requirements
python 3.5.3
numpy 1.11.1
scipy 0.19.0

On win7 it was reported to work with anaconda, so there would be no need to set these requirements up yourself.


3) Setup
Either you want to work with git and keep yourself up to date this way, then you should use https://github.com/Bloodmallet/bloodystats.git to clone the repository. Or you don't want that hassle and just download the whole package from https://github.com/Bloodmallet/bloodystats. Unpack the content into your simulationcraft directory. So that the following structure reflects your system (with probably different directory names)
>path_to_simc_directory/simc_directory/simc.exe
>path_to_simc_directory/simc_directory/bloodystats/bloodystats.py

Test your setup using cmd (or powershell) on windows.
  - open the basic Commandline from Windows by Shift+right clicking on blank space inside your 'Bloodystats' directory
  - enter 'python bloodystats.py'
If your setup works, you'll see multiple new lines and a newline added every few seconds with new numbers.


4) Examples
'python bloodystats.py' uses all data from settings.py to make a run. Change your wanted values in that file first if you want to repeat these later on again or just change one thing at a time.
'python bloodystats.py --class shaman' will use settings.py but will overwrite the class setting to use shaman. Well if you have something like beast_master as a spec bloodystats will put out an error telling you that your input wasn't valid. I mean...who've seen a beastmaster shaman anywhere?

For further params please read 'settings.py' or 'python bloodystats.py -h' or 'python bloodystats.py --help'


5) Bloodystats is able to run on different talent combinations within one run. You have two different ways of setting this up. Please note that the standard talent combination from the basic profiles from SimulationCraft wont be used.

using custom_talent_combinations.simc and settings.py:
  - enter your wanted talent combinations into "custom_talent_combinations.simc" as new lines
  - change 'talents = "WHATEVER"' in settings.py to 'talents = ""'
  - run bloodystats.py as always (probably 'python bloodystats.py')

using custom_talent_combinations.simc but no settings.py:
  - enter your wanted talent combinations into "custom_talent_combinations.simc" as new lines
  - run bloodystats.py using '--talents ""' ('python bloodystats.py --talents ""')

Example for "custom_talent_combinations.simc":
2112332
2112331
3231323

using built in talent combination generation:
  - two digit input will generate all dps talent combinations for the spec, where the last two dps rows are set to the value you input (1 left, 2 middle, 3 right) example: '--talents 21' ('python bloodystats.py --talents 21')
  - seven character input will generate all dps talent combinations for the spec, where all x'ed positions are filled with dps talents

Due to the seven character input one beeing slightly tricky at first let me explain that further.
Example: '--talents 211xx23'
This input will generate 9 talent combinations IF both x are in rows with dps talents. It'll generate 3 talent combinations, if one x is a non dps row and it will generate only one talent combination, if both x are non dps rows.
Example: '--talents 2113323'
This input will make bloodystats run exactly one talent combination.


5) End
	
Feedback is highly appreciated!

Yours sincerely
Bloodmallet(EU)
