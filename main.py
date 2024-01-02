import csv
import random as r

live = []
dead = []
filebuilt = False


# Core object for setup and running the simulation
def setup_run():
    userinput = input("Character sheet file location: ")
    print(build(userinput))
    if not filebuilt:
        outoptions()
    print("")
    userinput = input("Would you like to include survivability scores in the simulation?\n(enter 'Y' for yes or 'N' for\
 no)")
    if userinput == "y" or input == "Y":
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
                    # Format for character list objects: [number, name, survivability, kills, Death in encounter, placement]
                    # Add Number
                    character = [i]
                    # Name and survivability
                    character.extend(row)
                    # Converting survivability to integer
                    character.append(int(character.pop(2)))
                    # Add Kills
                    character.append(0)
                    # Add encounter death
                    character.append(0)
                    # Add placement
                    character.append(0)
                    live.append(character)
                    print("Success!")
            filebuilt = True
            return "Player build complete!"
    except:
        print("There was an error reading your file. Please ensure the file\naddress is correct and that the file is\n\
properly formatted.")
        filebuilt = False
        return "\nPlease select an action."


def simulation(surv):
    encounter = 0
    print("Starting simulation...")
    while len(live) > 1:
        encounter += 1

        print("Encounter #" + str(encounter) + ":")
        # Select players for an encounter
        p2i = None
        p1i = r.randint(0, len(live) - 1)
        while p2i == p1i or p2i is None:
            p2i = r.randint(0, len(live) - 1)

        # Calculate winner (survivability on/off)
        if surv:
            # With survivability
            divisor = live[p1i][2] + live[p2i][2]
            quotient = 1 / divisor
            wincondition = quotient * live[p1i][2]
            if r.random() < wincondition:
                # Player 1 wins
                live[p1i][3] = live[p1i][3] + 1
                print(live[p1i][1] + " beat " + live[p2i][1] + " in encounter #" + str(encounter) + ".")
                print(live[p2i][1] + " has been eliminated.")
                live[p2i][4] = encounter
                live[p2i][5] = len(live)
                dead.append(live[p2i].pop())
                print(live[p1i][1] + " now has", live[p1i][3], "kills.")
            else:
                # Player 2 wins
                live[p2i][3] = live[p2i][3] + 1
                print(live[p2i][1] + " beat " + live[p1i][1] + " in encounter #" + str(encounter) + ".")
                print(live[p1i][1] + " has been eliminated.")
                live[p1i][4] = encounter
                live[p1i][5] = len(live)
                dead.append(live[p1i].pop())
                print(live[p2i][1] + " now has", live[p2i][3], "kills.")
        else:
            # No survivability
            if r.random() < 0.5:
                # Player 1 wins
                live[p1i][3] = live[p1i][3] + 1
                print(live[p1i][1] + " beat " + live[p2i][1] + " in encounter #" + str(encounter) + ".")
                print(live[p2i][1] + " has been eliminated.")
                live[p2i][4] = encounter
                live[p2i][5] = len(live)
                dead.append(live[p2i].pop())
                print(live[p1i][1] + " now has", live[p1i][3], "kills.")
            else:
                # Player 2 wins
                live[p2i][3] = live[p2i][3] + 1
                print(live[p2i][1] + " beat " + live[p1i][1] + " in encounter #" + str(encounter) + ".")
                print(live[p1i][1] + " has been eliminated.")
                live[p1i][4] = encounter
                live[p1i][5] = len(live)
                dead.append(live[p1i].pop())
                print(live[p2i][1] + " now has", live[p2i][3], "kills.")
    return "Simulation complete!"


def exportresults():
    if filebuilt:
        try:
            with open("results.csv", 'x', newline="") as csvfile:
                csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_NONE)
                csvwriter.writerow(['#'], ['Name'], ['Survivability'], ['Kills'], ['Encounter of Death'], ['Placement'])
                for i in live:
                    csvwriter.writerow([live[i][0]], [live[i][1]], [live[i][2]], [live[i][3]], [live[i][4]], [live[i][5]])
        except:
            print("We encountered an error creating your file. Ensure that there is no file called 'results.csv' in this\n\
ogram's root folder, and try again. If you continue to see this error, inform the developers immediately.")
    else:
        print("It seems no simulation has been completed. Please select a different option.")
    outoptions()


def outoptions():
    # Follows simulation completion
    print("Your options are:")
    print("1)  Export results of the simulation")
    print("2)  Run another simulation")
    print("3)  Exit the program\n")
    userinput = input("Please enter your choice as a single digit 1-3:")
    if userinput == "1":
        # Build and export results spreadsheet
        exportresults()
    elif userinput == "2":
        # Restart simulation
        setup_run()
    elif userinput == "3":
        print("Closing the program...")
        exit()

# Welcome and input prompt
print("Welcome to Battle Royale Simulator Version 2!")
print("To begin, please enter the absolute location of your character .CSV file.")
print("For information on how to properly create and format this spreadsheet\nfile, please find the 'README.txt' file\n\
in this project's root.")
setup_run()
