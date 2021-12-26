# Game Tracker

A program that nicely calculates and keeps track of game rankings, storing them in a table
and a CSV save file.

# GETTING STARTED:

1) Clone this repository and import beautifultable from requirements.txt into your environment.

2) Open setup.py in a command line tool or IDE of your choice.

3) Follow the instructions in setup.py to add the desired players to your save files.

4) Open game_tracker.py in a command line tool or IDE of your choice.

5) Follow the instructions in the program to add a game, clear data, merge data, or predict a game.

6) To add additional players, you can run setup.py at any time and select the amount of players you wish to add.

7) Standings can be viewed each time the program is run or in the standings.txt file created for each gametype. 

## A Note About Elo Rankings:

Elo rankings have been implemented to be used as an additional metric for rankings in an attempt to stabilize changes given that players may be at different levels of skills and may play one another in uneven amounts. Note that by default, all players start with an Elo ranking of 1500, which naturally gets more accurate the more games are played.

## Issues and Errors:

It's important to note that if the names or locations of save files are changed, the program will be unable to run. If this is the case, please rename and move save files back into the same directory as game_tracker.py, or recreate them in setup.py.
