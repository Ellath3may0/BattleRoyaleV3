import csv
import random as r

live = []
dead = []
filebuilt = False


class Player:
    number = None
    name = None
    survivability = None
    kills = 0
    encounter_of_death = None
    placement = None

    def __init__(self, number, name, survivability):
        self.number = number
        self.name = name
        self.survivability = survivability


# Core object for setup and running the simulation
def setup_run():
    userinput = input("Character sheet file location: ")
    print(build(userinput))
    if not filebuilt:
        outoptions()
    print("")
    userinput = input("Would you like to use weighted randomizers in the simulation?\n(enter 'Y' for yes or 'N' for\
 no)")
    if userinput.lower() == "y":
        surv = True
    else:
        surv = False
    print(simulation(surv))
    outoptions()


# Build list of live players from .CSV input.
def build(filelocation):
    global live
    global filebuilt
    print("Starting character build...")
    try:
        with open(filelocation, newline="") as inputFile:
            filereader = csv.reader(inputFile, quotechar="|")
            for i, row in enumerate(filereader):
                if i >= 1:
                    print("Building player", i, "...", end="")
                    # Initialise new player object and add it to the list
                    player = Player(i, row[0], int(row[1]))
                    live.append(player)
                    print("Success!")
            filebuilt = True
            inputFile.close()
            return "Player build complete!"
    except Exception:
        print("There was an error reading your file. Please ensure the file\naddress is correct and that the file is\n\
properly formatted.")
        filebuilt = False
        return "\nPlease select an action."


def simulation(surv):
    global live
    global dead
    encounter = 0
    print("Starting simulation...")
    while len(live) > 1:
        encounter += 1

        print("Encounter #" + str(encounter) + ":")
        # Select players for an encounter
        player2index = None
        player1index = r.randint(0, len(live) - 1)
        while player2index == player1index or player2index is None:
            player2index = r.randint(0, len(live) - 1)

        # Calculate winner (survivability on/off)
        if surv:
            # With survivability
            total = live[player1index].survivability + live[player2index].survivability
            if r.random() < live[player1index].survivability / total:
                # Player 1 wins
                winner = player1index
                loser = player2index
            else:
                # Player 2 wins
                winner = player2index
                loser = player1index
        else:
            # No survivability
            if r.random() < 0.5:
                # Player 1 wins
                winner = player1index
                loser = player2index
            else:
                # Player 2 wins
                winner = player2index
                loser = player1index
            # Result of encounter
        live[winner].kills += 1
        print(live[winner].name + " beat " + live[loser].name + " in encounter #" + str(encounter) + ".")
        print(live[loser].name + " has been eliminated.")
        live[loser].encounter_of_death = encounter
        live[loser].placement = len(live)
        print(live[winner].name + " now has", live[winner].kills, "kills.")
        dead.append(live.pop(loser))
    live[0].placement = 1
    return "Simulation complete!"


def exportresults():
    global live
    if filebuilt:
        try:
            with open("results.csv", 'x', newline="") as csvfile:
                csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_NONE)
                csvwriter.writerow(['#', 'Name', 'Survivability', 'Kills', 'Encounter of Death', 'Placement'])
                for i, player in enumerate(live):
                    csvwriter.writerow([player.number, player.name, player.survivability, player.kills,
                                        player.encounter_of_death, player.placement])
                for i, player in enumerate(reversed(dead)):
                    csvwriter.writerow([player.number, player.name, player.survivability, player.kills,
                                        player.encounter_of_death, player.placement])
                print("\nResults exported successfully\n")
        except Exception:
            print("We encountered an error creating your file. Ensure that there is no file called 'results.csv' in\n\
this program's root folder, and try again. If you continue to see this error, inform the developers immediately.")
    else:
        print("It seems no simulation has been completed. Please select a different option.")
    outoptions()


def outoptions():
    # Follows simulation completion
    print("Your options are:")
    print("1)  Export results of the simulation")
    print("2)  Run another simulation")
    print("3)  Exit the program\n")
    while True:
        userinput = input("Please enter your choice as a single digit 1-3:")
        if userinput == "1":
            # Create and export results spreadsheet
            exportresults()
        elif userinput == "2":
            # Restart simulation
            setup_run()
        elif userinput == "3":
            print("Closing the program...")
            exit()
        else:
            print("We didn't recognise that response. Please try again.")


# Welcome and input prompt
print("Welcome to Battle Royale Simulator Version 2!")
print("To begin, please enter the absolute location of your character .CSV file.")
print("For information on how to properly create and format this spreadsheet\nfile, please find the 'README.txt' file\n\
in this project's root.")
setup_run()
