"""
A program that calculated and keeps track of game standings,
printing them nicely in a table and storing them
in a CSV file.
"""
from beautifultable import BeautifulTable
from shutil import copyfile
from operator import itemgetter
import csv

# Stores the paths to files used
savefile = ""
standings = ""
# Stores player data in memory
savedata = {}


def main():
    global savefile, standings  # Both of these variables need to be updated in main

    # Allows for two different standings files to be kept
    prompt = "Would you like to load the tournament or league save data? "

    # Checks user input for either words, updating file path variables accordingly
    if input_checker(["tournament", "league"], prompt) == "tournament":
        standings = "C:/Users/nshaf/Desktop/Other/CS/Personal Stuff/Game Tracker/TournamentStandings.txt"
        savefile = "C:/Users/nshaf/Desktop/Other/CS/Personal Stuff/Game Tracker/tournamentsavedata.csv"

    else:
        standings = "C:/Users/nshaf/Desktop/Other/CS/Personal Stuff/Game Tracker/LeagueStandings.txt"
        savefile = "C:/Users/nshaf/Desktop/Other/CS/Personal Stuff/Game Tracker/leaguesavedata.csv"

    # Reads data from the CSV save file into memory
    data_read(savedata, savefile)

    # Begins the main program that interacts with the user
    prompt = "Would you like to add a game, clear data, merge data, or exit?"
    user_program(prompt)


# Main program, interacts with user.
def user_program(prompt):
    global savedata, standings, savefile  # These variables may need to be updated depending on used selection

    # Checks user input for the mode they want to use
    task = input_checker(["game", "add", "clear", "merge", "exit", "no"], prompt)

    # User wants to add a game. Appropriate questions and calculations are made.
    if task == "game" or task == "add":
        # Asks user for the winner and loser, ensuring that only a name in savedata is referenced
        prompt = "Who won? "
        winner = input_checker(savedata, prompt, errormsg="Player not found. Please try again.\n")
        prompt = "Who lost? "
        loser = input_checker(savedata, prompt, errormsg="Player not found. Please try again.\n")
        # Asks user for goals scored, ensuring that only integers are entered.
        # Will prompt the user if there is an error.
        while True:
            try:
                wingoals = int(input(f"How many goals did {winner} score? ").rstrip())
                losgoals = int(input(f"How many goals did {loser} score? ").rstrip())
                break
            except ValueError:
                print("Please use proper integer input (i.e 10).\n")

        # Various calculations are made for standings file
        savedata[winner]['Games Played'] += 1
        savedata[winner]['Wins'] += 1
        savedata[winner]['Goals Scored'] += wingoals
        savedata[winner]['Goals Against'] += losgoals
        savedata[winner]['Win %'] = round((savedata[winner]['Wins'] /
                                           (savedata[winner]['Wins'] + savedata[winner]['Losses'])), 3)
        savedata[winner]['Goal Differential'] = savedata[winner]['Goals Scored'] - savedata[winner][
            'Goals Against']
        savedata[loser]['Games Played'] += 1
        savedata[loser]['Losses'] += 1
        savedata[loser]['Goals Scored'] += losgoals
        savedata[loser]['Goals Against'] += wingoals
        savedata[loser]['Win %'] = round((savedata[loser]['Wins'] /
                                          (savedata[loser]['Wins'] + savedata[loser]['Losses'])), 3)
        savedata[loser]['Goal Differential'] = savedata[loser]['Goals Scored'] - savedata[loser]['Goals Against']

        # Repeats the program by asking the user to select another course of action
        user_program("Would you like to add another game, clear data, merge data, or exit? ")

    elif task == "no" or task == "exit":  # User does not want to add data
        print("Exiting program...")
        data_write()  # Writes data to save and standings files

    elif task == "clear":  # User wants to clear saved data

        # Ensures the user didn't make a typo, as this action is irreversible
        prompt = "Are you sure? This can't be undone. "

        # Checks user input to see if a yes or no is entered
        zeroconfirm = input_checker(["yes", "no"], prompt)

        if zeroconfirm == "yes":  # The user still wants to clear data
            # Copies save file to downloads
            copyfile(savefile, "C:/Users/nshaf/Downloads/savedata.csv")
            print("Save file has been copied as a precautionary measure to your downloads folder.")

            # Zeros out data in memory
            for player in savedata:
                for val in savedata[player]:
                    if savedata[player][val] not in savedata:
                        savedata[player][val] = 0

            data_write()  # Writes data back into standings and save data files
            print("\nSuccessfully zeroed file.\n")

            # Repeats the program by asking the user to select another course of action
            prompt = "Now would you like to add a game, clear data, merge data, or exit? "
            user_program(prompt)

        elif zeroconfirm == "no":  # The user no longer wants to clear data
            print("Zero cancelled.\n")

            # Repeats the program by asking the user to select another course of action
            prompt = "So would you like to add another game, clear data, merge data, or exit? "
            user_program(prompt)

    elif task == "merge":  # User wants to merge tournament data into league data

        # If the program is already open in league mode, writing tournament data into it can be done easily
        if "league" in savefile:
            # Ensures the user didn't make a typo, as this action is irreversible
            prompt = "Are you sure? This can't be undone. "

            # Checks user input to see if a yes or no is entered
            mergeconfirm = input_checker(["yes", "no"], prompt)

            if mergeconfirm == "yes":  # The user still wants to clear data
                # Copies save file to downloads
                copyfile(savefile, "C:/Users/nshaf/Downloads/savedata.csv")
                print("Save file has been copied as a precautionary measure to your downloads folder.")

                # Will store path to tournament save data
                altpath = "C:/Users/nshaf/Desktop/Other/CS/Personal Stuff/Game Tracker/tournamentsavedata.csv"
                # Will store tournament data in memory
                altsavedata = {}

                # Reads tournament data into memory
                data_read(altsavedata, altpath)

                k = 2  # Weighted multiplier for tournament data into league data

                # Adds tournament statistics to league data, multiplying everything by k except win %
                for player in altsavedata:
                    for val in altsavedata[player]:
                        if altsavedata[player][val] not in altsavedata:
                            if val == "Win %":
                                savedata[player][val] = altsavedata[player][val]
                            else:
                                savedata[player][val] += (altsavedata[player][val] * k)

                data_write()  # Writes data back into standings and save data files
                print("\nSuccessfully merged files.\n")

                # Repeats the program by asking the user to select another course of action
                prompt = "Now would you like to add a game, clear data, or exit? "
                user_program(prompt)

            elif mergeconfirm == "no":  # The user no longer wants to merge data
                print("Merge cancelled.\n")

                # Repeats the program by asking the user to select another course of action
                prompt = "So would you like to add another game, clear data, merge data, or exit? "
                user_program(prompt)
        else:  # If the program is open in tournament mode, it must be changed into league mode
            print("Sorry, you can only merge tournament data into league data.\n")

            # Asks the user if they'd like to reload the program
            prompt = "Would you like to reload the program into tournament mode?"

            # The user wants to reload the program.
            # Standings and save file paths are updated to league data, which is then read into memory
            if input_checker(["yes", "no"], prompt) == "yes":
                standings = "C:/Users/nshaf/Desktop/Other/CS/Personal Stuff/Game Tracker/LeagueStandings.txt"
                savefile = "C:/Users/nshaf/Desktop/Other/CS/Personal Stuff/Game Tracker/leaguesavedata.csv"
                data_read(savedata, savefile)
                print("\nSuccessfully reloaded data.\n")

                # Now that the program is in league mode, data can be merged with no problem
                prompt = 'So would you like to merge data? Please type "merge" to proceed.'
                user_program(prompt)

            else:  # The user does not want to reload the program into league mode
                prompt = "\nSo would you like to add another game, clear data, or exit? "
                user_program(prompt)


# Recursively checks for correct user input given a list of responses, a prompt,
# and an optional error message. If no error message is provided, the default will be used.
def input_checker(responses, prompt, errormsg="Sorry! I don't recognize your input. Please try again. \n"):
    # Prompts the user for their input and standardizes it
    rawinput = input(prompt).rstrip().lower()

    # Iterates through list of proper responses, returning one if there is a match
    for response in responses:
        if response in rawinput:
            return response

    # Since no match was found, the error message is printed and the function is returned to be rerun
    print(errormsg)
    return input_checker(responses, prompt, errormsg)


# Writes savedata from memory to save and standings files
def data_write():
    # Creates statistics table, setting default cell width and table style
    table = BeautifulTable(maxwidth=150)
    table.set_style(BeautifulTable.STYLE_SEPARATED)

    # Header rows for the table
    table.columns.header = ["Person", "Wins", "Losses", "Games Played", "Win %",
                            "Goals Scored", "Goals Against", "Goal Differential"]

    # Writes updated data back into CSV file and into the statistics table
    with open(savefile, 'w', newline='') as file:
        fields = table.columns.header
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()  # Rewrites header of CSV file
        for player in savedata:
            currow = []  # A list representing each row in the table is created
            for val in savedata[player]:
                currow.append(savedata[player][val])
            table.rows.append(currow)  # The list is added as a row in the table
            writer.writerow(savedata[player])  # The updated data is written to the CSV file

    # Column rows for the table
    table.rows.header = ["1", "2", "3", "4"]

    # Sorts the table by win percentage first, then goal differential
    table.rows.sort((itemgetter("Win %", "Goal Differential")), reverse=True)

    # Writes table to output standings file
    with open(standings, 'w') as output:
        output.write(str(table))


# Reads the saved CSV file into memory
def data_read(datastruct, path):
    with open(path, 'r') as file:
        reader = csv.DictReader(file)
        # An entry for each player is added with a nested dict for storing statistics.
        for row in reader:
            datastruct[row['Person']] = row

    # Casts statistics as floats
    for player in datastruct:
        for val in datastruct[player]:
            if datastruct[player][val] not in datastruct:  # To avoid casting a player name
                datastruct[player][val] = float(datastruct[player][val])


if __name__ == "__main__":
    main()
