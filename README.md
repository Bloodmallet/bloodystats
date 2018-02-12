Bloodystats
===========

> Automatation tool to calculate best secondary stat rating distribution for dps for a given profile of a World of Warcraft character using SimulationCraft. It's designed in a way that should make it easy to add different approaches to solve this problem.

## Requirements
You need a working SimulationCraft version, Python 3.5 or newer and to install the requirements.txt.

## Download
Download or clone this repository into your SimulationCraft directory. `simulationcraft\bloodytrinkets`

## Setup
Start your python environement. Install dependencies.
```sh
$ <env_name>\Scripts\active
(<env_name>)$ pip install -U -r .\requirements.txt
```

`pip freeze` should return something like this:
```
numpy==1.14.0
scipy==1.0.0
-e git+https://github.com/Bloodmallet/simc_support.git@0e619764a0ccd919386ea50839460eb2f5c16e53#egg=simc_support
```

## Getting started
Edit settings.py to your liking using any text editor. Start your python environement. Start bloodystats.
```sh
$ <env_name>\Scripts\active
(<env_name>)$ python .\bloodystats.py
```

## Examples
`python bloodystats.py` uses all data from settings.py to calculate one data set. Change your wanted values in that file first, if you want to repeat these later on again or just change one entry at a time.
`python bloodystats.py --class shaman` will use settings.py but will overwrite the class setting to be "shaman" instead. Pay attention to the class and spec combination. If your settings.py does have beast_master set as spec, bloodystats will put out an error, when you try the previously mentioned input. There is no beast_master shaman.

If no custom_characzer_stats are provided bloodystats attempts to use the standard profiles of SimulationCraft.

For further params please read `settings.py` or `python bloodystats.py -h` or `python bloodystats.py --help`.

Take special note about possible different talent combinations. Bloodystats allows several short hands and different input to allow a quick setup. You have two different ways of using these. Please note that the standard talent combination from the basic profiles from SimulationCraft wont be used.

### Using custom_talent_combinations.simc and settings.py:
  - enter your wanted talent combinations into "custom_talent_combinations.simc" as new lines
  - change `talents = "WHATEVER"` in settings.py to `talents = ""`
  - start bloodystats.py as always (probably `python bloodystats.py`)

### Using custom_talent_combinations.simc but no settings.py:
  - enter your wanted talent combinations into "custom_talent_combinations.simc" as new lines
  - start bloodystats.py using `python bloodystats.py --talents ""`

### Example for "custom_talent_combinations.simc":
```
2112332
2112331
3231323
```

### Using built in talent combination generation:
  - two digit input will generate all dps talent combinations for the spec, where the last two dps rows are set to the value you input (1 left, 2 middle, 3 right) example: `--talents 21` (`python bloodystats.py --talents 21`)
  - seven character input will generate all dps talent combinations for the spec, where all x'ed positions are filled with dps talents

Due to the seven character input one beeing slightly tricky at first let me explain that further.
Example: `--talents 211xx23`
This input will generate 9 talent combinations IF both x are in rows with dps talents. It'll generate 3 talent combinations, if one x is a non dps row and it will generate only one talent combination, if both x are non dps rows.
Example: `--talents 2113323`
This input will make bloodystats run exactly one talent combination.

## Result
A successful run creates a txt file in the `results/` directory. Here you can the best performing secondary combinations. Best performing in this case means "within 1% of the best found value".
```
1001331 2244768 12371 8371  12371 3871
        2244768 12371 8371  12371 3871
        2244246 10371 10371 12371 3871
```
Lines starting with a number instead of spaces indicate the start of a new calculation group. The initial number represents the talent combination. Followed by DPS, crit, haste, mastery, and finally versatility. Lines starting with empty spaces are saved calculated values that performed within 1% of the best secondary rating combination. These should help to get an impression of how important or unimportant it really is to perfectly match the best distribution.

The values of the example above are explained again in this table.

| talent combination | dps | crit | haste | mastery | versatility |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1001331 | 2244768 | 12371 | 8371 | 12371 | 3871 |
| | 2244768 | 12371 | 8371 | 12371 | 3871 |
| | 2244246 | 10371 | 10371 | 12371 | 3871 |

## Development
You can start right away. The strongest need right now would probably be the implementation of tests. But as I want to merge my different projects into one with the coming Battle for Azeroth expansion, be prepared, that those are probably going to see heavy changes. Anyway, I'd love to help if someone is interested in improving or adding something.

## Contact
General support can be found at https://discord.gg/tFR2uvK in the channel #bloodytools. In addition to this you can easily open [issues in the repo](https://github.com/Bloodmallet/bloodystats/issues).
