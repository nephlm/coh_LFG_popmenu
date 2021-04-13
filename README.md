# coh_LFG_popmenu


## What it is.  

A highly complicated set of favorites for AboveTheChemist's badge list and title setting popmenu for city of heroes. 

It's designed to provide useful information to someone watching the LFG channel and wondering if this character has badge for the just posted Sutter's TF.  Rather than having to remember or look up what badge that TF provides (and which section TF badges are in) it can be accessed by `Taskforces -> (Level range) -> (Contact) -> (Taskforce Name) -> Badge`.

Giant monsters are looked up by name of monsters and trials group all badges under the trial name. 

## AboveTheChemist's original work.

The original work is here.
https://forums.homecomingservers.com/topic/24454-atcs-badge-list-popmenu/

I believe ATC is github user https://github.com/n15g.  I don't see a repo used to build the menu's but he does maintain repo of badge data here:  https://github.com/n15g/coh-content-db-homecoming.  It's in typescript and when I started this the idea of converting that data to a python readable form, seemed annoying.  
## How to generate a new menu.

Main thing to run is `build_menu.py`  It will write the menu in `build/BadgeSetListNeph.mnu`

## All the fiddly bits.

`reference/BadgeSetList.mnu` is AboveTheChemist's original file.  When he releases a new one that file needs to broken to a head and footer. The file split inside the favorites menu.

Be sure to update the header with info about the neph version.  Header and footer go into the `data` directory with names of `LFGPopmenu_header.txt` and `LGFPopmenu_footer.txt`.

`import_data.py` just converts csv files to json.  Shouldn't have to be written once all the csv files have been converted.  Update the `input_file` and `output_file` hard coded values in the file ans needed.  Yeah, it's that kind of project.

`extract_badge_data.py`  uses the reference menu to extract all badges and populate `all_badges.json`.  I wrote that script halfway through the project so it's used by trials.  One day I'll go back and update task forces and giant monsters to use it.  

The csv files is data collected from wikis.  Spreadsheets were an easier interface that writing json directly, but re-transforming some datasets is not a good idea.  Specifically many contain a list of abbreviations.  This data isn't used yet, but it is a nested list inside the dicts.  There were regexes applied to the output of the json transformation.

In vscode
```
"Abbreviation":\s*"(.*)" -> "Abbreviation": ["$1"]
"Abbreviation": \[(.*)(,)\s*(.*)\] -> "Abbreviation": [$1", "$3]
```
The second one only works with two abbreviations, but that's the most I have so far.

## Roadmap

* Trials are still be worked on.
* Defeats by enemy group.
* Named defeats by name and under enemy group
* Abbreviations