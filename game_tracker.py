"""
A program that calculates and keeps track of game standings,
printing them nicely in a table and storing them
in a CSV file.
"""
from beautifultable import BeautifulTable
from shutil import copyfile
from operator import itemgetter
import csv
import os

# Stores the paths to files used
savefile = ""
standings = ""
downloads = os.path.join(os.getenv('USERPROFILE'), 'Downloads')
gametype = ""
# Stores player data in memory
savedata = {}


def main():
    global savefile, standings, gametype  # These variables need to be updated in main

    # Allows for two different standings files to be kept
    prompt = "Would you like to load the tournament or league save data? "

    # Checks user input for either words, updating file path variables accordingly
    gametype = input_checker(["tournament", "league"], prompt)
    savefile = os.path.dirname(os.path.realpath(__file__)) + r"\{}savedata.csv".format(gametype)
    standings = os.path.dirname(os.path.realpath(__file__)) + r"\{}standings.txt".format(gametype)

    # Reads data from the CSV save file into memory
    data_read(savedata, savefile)

    # Begins the main program that interacts with the user
    prompt = "Would you like to add a game, clear data, merge data, predict a game, remove a player, or exit?"
    user_program(prompt)


# Main program, interacts with user.
def user_program(prompt):
    global savedata, standings, savefile  # These variables may need to be updated depending on user selection

    # Checks user input for the mode they want to use
    task = input_checker(["game", "add", "clear", "merge", "exit", "no", "predict", "expect",
                          "delete", "drop", "remove"], prompt)

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
                wingoals = int(input(f"How many goals did {winner.capitalize()} score? ").rstrip())
                losgoals = int(input(f"How many goals did {loser.capitalize()} score? ").rstrip())
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

        if "league" in savefile:
            elo(savedata, winner, loser, update=True)
        # Repeats the program by asking the user to select another course of action
        user_program("\nWould you like to add another game, clear data, merge data, predict a game, "
                     "remove a player, or exit? ")

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
            copyfile(savefile, downloads + f"/{gametype}savedata.csv")
            print("Save file has been copied as a precautionary measure to your downloads folder.")

            # Zeros out data in memory
            for player in savedata:
                for val in savedata[player]:
                    if savedata[player][val] not in savedata:
                        savedata[player][val] = 0

            data_write()  # Writes data back into standings and save data files
            print("\nSuccessfully zeroed file.\n")

            # Repeats the program by asking the user to select another course of action
            prompt = "Now would you like to add a game, merge data, predict a game, remove a player, or exit? "
            user_program(prompt)

        elif zeroconfirm == "no":  # The user no longer wants to clear data
            print("Zero cancelled.\n")

            # Repeats the program by asking the user to select another course of action
            prompt = "Would you like to add a game, merge data, predict a game, remove a player, or exit? "
            user_program(prompt)

    elif task == "merge":  # User wants to merge tournament data into league data

        # If the program is already open in league mode, writing tournament data into it can be done easily
        if gametype == "league":
            # Ensures the user didn't make a typo, as this action is irreversible
            prompt = "Are you sure? This can't be undone. "

            # Checks user input to see if a yes or no is entered
            mergeconfirm = input_checker(["yes", "no"], prompt)

            if mergeconfirm == "yes":  # The user still wants to clear data
                # Copies save file to downloads
                copyfile(savefile, downloads + f"/{gametype}savedata.csv")
                print("Save file has been copied as a precautionary measure to your downloads folder.")

                # Will store path to tournament save data
                altpath = os.path.dirname(os.path.realpath(__file__)) + r"\tournamentsavedata.csv"

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
                prompt = "Now would you like to add a game, clear data, predict a game, remove a player, or exit? "
                user_program(prompt)

            elif mergeconfirm == "no":  # The user no longer wants to merge data
                print("Merge cancelled.\n")

                # Repeats the program by asking the user to select another course of action
                prompt = "Would you like to add a game, clear data, predict a game, remove a player, or exit? "
                user_program(prompt)
        else:  # If the program is open in tournament mode, it must be changed into league mode
            print("Sorry, you can only merge tournament data into league data.\n")

            # Asks the user if they'd like to reload the program
            prompt = "Would you like to reload the program into tournament mode? "

            # The user wants to reload the program.
            # Standings and save file paths are updated to league data, which is then read into memory
            if input_checker(["yes", "no"], prompt) == "yes":
                standings = os.path.dirname(os.path.realpath(__file__)) + r"\leaguestandings.txt"
                savefile = os.path.dirname(os.path.realpath(__file__)) + r"\leaguesavedata.csv"
                data_read(savedata, savefile)
                print("\nSuccessfully reloaded data.\n")

                # Now that the program is in league mode, data can be merged with no problem
                prompt = 'So would you like to merge data? Please type "merge" to proceed.'
                user_program(prompt)

            else:  # The user does not want to reload the program into league mode
                prompt = "\nWould you like to add a game, clear data, predict a game, remove a player, or exit? "
                user_program(prompt)

    elif task == "predict" or task == "expect":
        if gametype == "league":
            # Asks user for two players, ensuring that only a name in savedata is referenced
            prompt = "Player one: "
            p1 = input_checker(savedata, prompt, errormsg="Player not found. Please try again.\n")
            prompt = "Player two: "
            p2 = input_checker(savedata, prompt, errormsg="Player not found. Please try again.\n")
            print(elo(savedata, p1, p2))

            # Repeats the program by asking the user to select another course of action
            user_program("\nWould you like to add a game, clear data, "
                         "merge data, predict another game, remove a player, or exit? ")
        else:
            prompt = "You can only predict tournament games using league data. Would you like to proceed" \
                     " with using league data for predictions? "

            # Prompts the user, ensuring only a "yes" or "no" answer is received.
            if input_checker(["yes", "no"], prompt) == "yes":

                # Reads and stores league save data into memory
                leaguesavefile = os.path.dirname(os.path.realpath(__file__)) + r"\leaguesavedata.csv"
                leaguesavedata = {}
                data_read(leaguesavedata, leaguesavefile)

                print("\nSuccessfully imported league data rankings.\n")

                # Asks user for two players, ensuring that only a name in savedata is referenced
                prompt = "Player one: "
                p1 = input_checker(leaguesavedata, prompt, errormsg="Player not found. Please try again.\n")
                prompt = "Player two: "
                p2 = input_checker(leaguesavedata, prompt, errormsg="Player not found. Please try again.\n")
                print(elo(leaguesavedata, p1, p2))

                # Repeats the program by asking the user to select another course of action
                user_program("\nWould you like to add a game, clear data,"
                             "merge data, predict another game, remove a player, or exit? ")

            else:
                print("\nPrediction cancelled.")
                # Repeats the program by asking the user to select another course of action
                user_program("\nWould you like to add a game, clear data, "
                             "merge data, remove a player, or exit? ")

    elif task == "delete" or task == "drop" or task == "remove":

        # Ensures the user didn't make a typo, as this action is irreversible
        prompt = "Are you sure? This can't be undone. "

        # Checks user input to see if a yes or no is entered
        delconfirm = input_checker(["yes", "no"], prompt)

        if delconfirm == "yes":  # The user still wants to remove a player
            # Copies save file to downloads
            copyfile(savefile, downloads + f"/{gametype}savedata.csv")
            print("Save file has been copied as a precautionary measure to your downloads folder.")

            # Asks user for the winner and loser, ensuring that only a name in savedata is referenced
            prompt = "Which player would you like to remove? "
            rmplayer = input_checker(savedata, prompt, errormsg="Player not found. Please try again.\n")

            del savedata[rmplayer]

            data_write()  # Writes data back into standings and save data files
            print(f"\nSuccessfully removed {rmplayer.capitalize()}.\n")

            # Repeats the program by asking the user to select another course of action
            prompt = "Now would you like to add a game, clear data, merge data, predict a game, " \
                     "remove another player, or exit? "
            user_program(prompt)

        elif delconfirm == "no":  # The user no longer wants to clear data
            print("\nPlayer remove cancelled.\n")

            # Repeats the program by asking the user to select another course of action
            prompt = "So would you like to add a game, clear data, merge data, " \
                     "predict a game, remove a player or exit? "
            user_program(prompt)


# Predicts, or optionally updates, elo rankings for two players
def elo(datastruct, player1, player2, update=False):
    r1 = datastruct[player1]['Elo']  # Ranking for player 1
    r2 = datastruct[player2]['Elo']  # Ranking for player 2
    e1 = 1 / (1 + 10 ** ((r2 - r1) / 400))  # Expected chance of p1 beating p2
    e2 = 1 / (1 + 10 ** ((r1 - r2) / 400))  # Expected chance of p2 beating p1
    if update:
        global savedata
        # Weighted k values should be 25 for the first 30 games
        k1 = 25
        k2 = 25

        # If more than 30 games have been played, it should be decreased by 1/5 every game
        if savedata[player1]['Games Played'] > 30:
            k1 -= (savedata[player1]['Games Played'] - 30) / 5

        if savedata[player2]['Games Played'] > 30:
            k2 -= (savedata[player2]['Games Played'] - 30) / 5

        # Update elo values given the elo formula
        savedata[player1]['Elo'] = round(r1 + k1 * (1 - e1))
        savedata[player2]['Elo'] = round(r2 + k2 * (0 - e2))
        return

    # If update is not set, print out expected elo values
    return "{} has a {}% chance of beating {} in a game."\
        .format(player1.capitalize(), round(e1, 3), player2.capitalize())


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

    # League file has an elo category, but the tournament file doesn't
    if "league" in savefile:
        # Header rows for the table
        table.columns.header = ["Person", "Wins", "Losses", "Games Played", "Win %", "Elo",
                                "Goals Scored", "Goals Against", "Goal Differential"]

    else:
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

            # Add statistics to currow
            for val in savedata[player]:
                if val == "Person":
                    currow.append(savedata[player][val].capitalize())
                else:
                    currow.append(savedata[player][val])
            table.rows.append(currow)  # The list is added as a row in the table
            writer.writerow(savedata[player])  # The updated data is written to the CSV file

    if gametype == "league":
        # Sorts the table by win percentage first, then goal differential
        table.rows.sort((itemgetter("Win %", "Elo", "Goal Differential")), reverse=True)

    else:
        table.rows.sort((itemgetter("Win %", "Goal Differential")), reverse=True)

    print(table)

    # Writes table to output standings file
    with open(standings, 'w') as output:
        output.write(str(table))

    print("To view standings after closing this program, go to {}."
          .format(os.path.dirname(os.path.realpath(__file__)) + f"\{gametype}standings.txt"))


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

    # If this is the first time the program has been run, elo values will be 0.
    # They must be updated to the default of 1500.
    for player in datastruct:
        if "league" in savefile:
            if savedata[player]["Elo"] == 0:
                savedata[player]["Elo"] = 1500


if __name__ == "__main__":
    main()
