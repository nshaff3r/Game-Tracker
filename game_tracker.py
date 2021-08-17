"""
A quick program that keeps track of game standings,
printing them nicely in a table and storing them
in a CSV file. Error checking and design improvements
have not been implemented.
"""

from beautifultable import BeautifulTable
from shutil import copyfile
from operator import itemgetter
import csv

# Allows for two different standings files to be kept
gametype = input("Hi! Would you like to load the tournament or league save data?").rstrip().lower()
while True:
    if "tournament" in gametype:
        standings = "C:/Users/nshaf/Desktop/Other/CS/Personal Stuff/Game Tracker/TournamentStandings.txt"
        path = "C:/Users/nshaf/Desktop/Other/CS/Personal Stuff/Game Tracker/tournamentsavedata.csv"
        break
    elif "league" in gametype:
        standings = "C:/Users/nshaf/Desktop/Other/CS/Personal Stuff/Game Tracker/LeagueStandings.txt"
        path = "C:/Users/nshaf/Desktop/Other/CS/Personal Stuff/Game Tracker/leaguesavedata.csv"
        break
    else:
        print("Sorry! I don't recognize your input. Please try again! \n")
        gametype = input("Would you like to load the tournament or league save data?").rstrip().lower()

# Imports the saved CSV file into memory
savedata = {}
with open(path, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        savedata[row['Person']] = row

# Casts statistics as floats
for player in savedata:
    for val in savedata[player]:
        if savedata[player][val] not in savedata:
            savedata[player][val] = float(savedata[player][val])

# Main program, interacts with user. Note that error checking is not fully implemented.
task = input("Would you like to add a game? ").rstrip().lower()
while True:
    if "yes" in task:  # User wants to add a game. Appropriate questions and calculations are made.
        winner = input("Who won? ").rstrip().lower()
        loser = input("Who lost? ").rstrip().lower()
        wingoals = int(input(f"How many goals did {winner} score? ").rstrip())
        losgoals = int(input(f"How many goals did {loser} score? ").rstrip())
        savedata[winner]['Games Played'] += 1
        savedata[winner]['Wins'] += 1
        savedata[winner]['Goals Scored'] += wingoals
        savedata[winner]['Goals Against'] += losgoals
        savedata[winner]['Win %'] = round((savedata[winner]['Wins'] /
                                           (savedata[winner]['Wins'] + savedata[winner]['Losses'])), 3)
        savedata[winner]['Goal Differential'] = savedata[winner]['Goals Scored'] - savedata[winner]['Goals Against']
        savedata[loser]['Games Played'] += 1
        savedata[loser]['Losses'] += 1
        savedata[loser]['Goals Scored'] += losgoals
        savedata[loser]['Goals Against'] += wingoals
        savedata[loser]['Win %'] = round((savedata[loser]['Wins'] /
                                          (savedata[loser]['Wins'] + savedata[loser]['Losses'])), 3)
        savedata[loser]['Goal Differential'] = savedata[loser]['Goals Scored'] - savedata[loser]['Goals Against']
        task = input("\nWould you like to add another game? ").rstrip().lower()
    elif "no" in task:  # User does not want to add data
        print("Exiting program...")
        break
    elif "zero" in task:  # User wants to clear saved data
        if "yes" in input("Are you sure? This can't be undone. ").rstrip().lower():
            # Copies save file to downloads
            copyfile(path, "C:/Users/nshaf/Downloads/savedata.csv")
            print("File has been copied as a precautionary measure to your downloads folder.")
            # Zeros out data in memory, which will be written to the save file at the end
            # of the program. This could have also been accomplished with a function call
            # instead, but I preferred this approach.
            for player in savedata:
                for val in savedata[player]:
                    if savedata[player][val] not in savedata:
                        savedata[player][val] = 0
            print("\nSuccessfully zeroed file. Please re-run program to add data")
            break
        else:
            task = input("\nZero cancelled. Would you like to add a game? ").rstrip().lower()
    else:  # Unrecognized input
        print("Uh-oh! I didn't recognize your input. Please try again!\n")
        task = input("Would you like to add a game? ").rstrip().lower()

# Creates statistics table, setting default cell width and table style
table = BeautifulTable(maxwidth=150)
table.set_style(BeautifulTable.STYLE_SEPARATED)

# Header rows for the table
table.columns.header = ["Person", "Wins", "Losses", "Games Played", "Win %",
                        "Goals Scored", "Goals Against", "Goal Differential"]

# Writes updated data back into CSV file and into the statistics table
with open(path, 'w', newline='') as file:
    fields = table.columns.header
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()  # Rewrites header of CSV file
    for player in savedata:
        # A list representing each row in the table is created
        currow = []
        for val in savedata[player]:
            currow.append(savedata[player][val])
        table.rows.append(currow)  # The list is added as a row in the table
        writer.writerow(savedata[player])  # The updated data is written to the CSV file

# Column rows for the table
table.rows.header = ["1", "2", "3", "4"]
# Sorts the table by win percentage first, then goal differential
table.rows.sort((itemgetter("Win %", "Goal Differential")), reverse=True)

# Writes table to output file
with open(standings, 'w') as output:
    output.write(str(table))
