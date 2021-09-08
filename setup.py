import os
from game_tracker import input_checker
from sys import exit


# Creates and zeros save files
def writer(gametype):
    global playernames  # Player names can be stored so they don't have to be retyped

    # Save files should be in the same directory as setup.py
    dir = os.path.dirname(os.path.realpath(__file__)) + "\{}savedata.csv".format(gametype)

    # League game types require an additional statistic of Elo rankings
    if gametype == "league":
        header = "Person,Wins,Losses,Games Played,Win %,Elo,Goals Scored,Goals Against,Goal Differential"
        stats = 8
    else:
        header = "Person,Wins,Losses,Games Played,Win %,Goals Scored,Goals Against,Goal Differential"
        stats = 7

    # Checks if save file already have data written
    data = 'w'

    try:
        with open(dir, 'r') as file:
            reader = file.read()
            if reader[:6] == "Person":
                data = 'a'
    except FileNotFoundError:
        pass

    with open(dir, data) as file:
        # Asks user for goals scored, ensuring that only integers are entered.
        # Will prompt the user if there is an error.
        while True:
            try:
                players = int(input(f"\nHow many players would you like to add to the {gametype} file? ").rstrip())
                break
            except ValueError:
                print("Please use proper integer input (i.e 4).\n")

        # The header should only be written if the save file is empty
        if data == 'w':
            # Writes header to csv save file
            file.write(header + '\n')

        # If the amount of players entered for the first file
        # is equal to the amount of players needed for the second.
        if len(playernames) == players and len(playernames) != 0:
            prompt = "Would you like to use the same players for both files? "
            if input_checker(["yes", "no"], prompt) == "yes":
                for player in playernames:
                    file.write('\n' + player + ",0.0" * stats + '\n')
                return

        # Otherwise, prompt the user for the names of the players
        for player in range(players):
            name = input(f"Player {player + 1} name: ").lower().rstrip()
            playernames.append(name)
            file.write(name + ",0.0" * stats + '\n')


print("This program should only be used for creating new save files or adding players\n"
      "to existing ones. If you'd like to clear already existing save data,\n"
      'use the "zero" function in game_tracker.py.', end=' ')

# Prompts the user and ensures a response of "yes" or "no" is received
prompt = "Are you sure you'd like to proceed? "
if input_checker(["yes", "no"], prompt) == "no":
    exit("Exiting program...")

playernames = []  # Stores player names so the user doesn't need to enter them twice

# Creates tournament and league csv save files.
writer("tournament")
writer("league")

print("\nSuccess. You may now close this program and run game_tracker.py.")
