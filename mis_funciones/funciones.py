from . import datos
import random

def center_string(string, width=140):
    spaces = (width - len(string)) // 2
    centered_string = " " * spaces + string + " " * spaces
    return centered_string
def clear():
    print("\033[H\033[J", end="")


# def playGame():
#     while datos.game_round <= datos.maxRounds:

def setGamePriority(mazo):
    random.shuffle(mazo)
    for i in range(len(datos.game)):
        datos.players[datos.game[i]]["priority"] = i+1
        maxim = datos.players[datos.game[i]]["priority"]
    for dni in datos.game:
        # cambiar como se gestiona la prioridad mas adelante
        datos.players[dni]["cards"].append(mazo[0])
        mazo.remove(mazo[0])
        if datos.players[dni]["priority"] == maxim:
            datos.players[dni]["bank"] = True
        print(datos.players[dni])

def resetPoints():
    for dni in datos.game:
        datos.players[dni]["points"] = 20

def checkMinimum2PlayersWithPoints():
    two_players = len(datos.game)
    for dni in datos.game:
        if datos.players[dni]["points"] == 0:
            two_players -= 1
    if two_players < 2:
        print("Not enough players with points")

def orderAllPlayers():
    # preguntar al Jordi sobre esta funcion
    for i in range(len(datos.game)-1):
        for j in range(len(datos.game)-i-1):
            if datos.players[datos.game[j]]["priority"] < datos.players[datos.game[j+1]]["priority"]:
                aux = datos.game[j]
                datos.game[j] = datos.game[j+1]
                datos.game[j+1] = aux

def setBets():
    # preguntar como funciona esto
    print("Hola")

def getOpt(textOpts="", inputOptText="", rangeList=[], exceptions=[]):
    print(textOpts)
    while True:
        try:
            option = input(inputOptText)
            if option.isdigit():
                option = int(option)
            if option not in rangeList and option not in exceptions:
                raise ValueError("Invalid option".center(140,"="))
            else:
                return option
        except ValueError as e:
            print(e)
            input("".ljust(58)+"Press enter to continue")

def addRemovePlayers():
    textOpts = datos.space + "1)New Human Player" + "\n" + datos.space + "2)New Bot" + \
               "\n" + datos.space + "3)Show/Remove Players" + "\n" + datos.space + "4)Go Back"
    inputOptText = datos.space + "Option: "
    option_range = [1, 2, 3]
    exception = [4]
    option = getOpt(textOpts, inputOptText, option_range, exception)
    return option

def newPlayer(dni, name, profile, human):
    player_data = (dni, {"name": name, "human": human, "bank": False, "initialCard": "", "priority": 0,
                         "type": profile, "bet": 4, "points": 0, "cards": [], "roundPoints": 0})
    return player_data

def setNewPlayer(human = True):
    while True:
        try:
            name = input(datos.space+"Name: ")
            if not name.isalpha():
                raise ValueError(datos.space + "Incorrect name, enter a name that is not empty with only letters")
            dni = input(datos.space+"NIF: ")
            if not len(dni) == 9 or not dni[:8].isdigit() or not dni[8].isalpha() \
               or not datos.letrasDni[int(dni[:8])%23] == dni[8].upper():
                raise ValueError(datos.space + "Wrong NIF")
            textOps = datos.space+"Select your Profile:\n"+\
                                        datos.space+"1)Cautious\n"+\
                                        datos.space+"2)Moderated\n"+\
                                        datos.space+"3)Bold\n"
            inputOptText = datos.space+"Option: "
            option_range = [1,2,3]
            exception = []
            option = getOpt(textOps,inputOptText,option_range,exception)
            if option == 1:
                profile = 30
            elif option == 2:
                profile = 40
            elif option == 3:
                profile = 50
        except ValueError as e:
            print(e)
            input(datos.space+"Enter to continue")
            clear()

def settings():
    textOpts = datos.space + "1)Set Game Players" + "\n" + datos.space + "2)Set Card's Deck" + \
               "\n" + datos.space + "3)Set Max Rounds (Default 5 Rounds)" + "\n" + datos.space + "4)Go Back"
    inputOptText = datos.space + "Option: "
    option_range = [1, 2, 3, 4]
    exception = []
    option = getOpt(textOpts, inputOptText, option_range, exception)
    return option


def setPlayersGame():
    print(datos.titulo_021)
    print("Select players".center(140, "*"))
    print("Bot Players".center(70)+"Human Players".center(70)+"\n"+"-"*140)
    players_data = ""
    bot_players = []
    human_players = []
    header = ("ID".ljust(20) + "Name".ljust(20) + "Type".ljust(20)).ljust(64) + "|".ljust(4)+\
             ("ID".ljust(20) + "Name".ljust(20) + "Type".ljust(20) + "\n" + "*" * 140).ljust(70)
    print(header)
    for dni in datos.players:
        player = datos.players[dni]
        if player["human"]:
            human_players.append({"dni": dni, "name": player["name"], "type": player["type"]})
        else:
            bot_players.append({"dni": dni, "name": player["name"], "type": player["type"]})
    if len(human_players) > len(bot_players):
        max_list = human_players
    else:
        max_list = bot_players
    for i in range(len(max_list)):
        if i < len(bot_players):
            players_data += bot_players[i]["dni"].ljust(20) + bot_players[i]['name'].ljust(20)
            if bot_players[i]["type"] == 30:
                players_data += "Cautious".ljust(20)
            elif bot_players[i]["type"] == 40:
                players_data += "Moderated".ljust(20)
            elif bot_players[i]["type"] == 50:
                players_data += "Bold".ljust(20)
        else:
            players_data += "".ljust(20) + "".ljust(20) + "".ljust(20)
        players_data += "\t|\t"
        if i < len(human_players):
            players_data += human_players[i]["dni"].ljust(20) + human_players[i]['name'].ljust(20)
            if human_players[i]["type"] == 30:
                players_data += "Cautious".ljust(20)
            elif human_players[i]["type"] == 40:
                players_data += "Moderated".ljust(20)
            elif human_players[i]["type"] == 50:
                players_data += "Bold".ljust(20)
            else:
                players_data += "".ljust(20) + "".ljust(20) + "".ljust(20)
        players_data += "\n"
    print(players_data)
    # Provisional ////
    # text = datos.space+"Enter ID to add a player to the game\n"+\
    #       datos.space+"Enter -ID to remove a player from the game\n"+\
    #       datos.space+"Enter sh to show actual players in game\n"+\
    #       datos.space+"Enter -1 to exit\n"
    # option_text = datos.space + "Option: "
    # option_range = [datos.players]
    # //// Provisional
    option = input(datos.space+"Enter ID to add a player to the game\n"+\
          datos.space+"Enter -ID to remove a player from the game\n"+\
          datos.space+"Enter sh to show actual players in game\n"+\
          datos.space+"Enter -1 to exit\n"+\
          datos.space+"Option: ")
    if len(option) == 9 and option[:8].isdigit() and option[8].upper().isalpha() \
            and option.upper() in datos.players and {option.upper():datos.players[option.upper()]} not in datos.game:
        if len(datos.game) <= 5:
            datos.game.append(option.upper())
            showPlayersGame()
        else:
            print(center_string("-Max number of players exceeded-"))
            input(center_string("Enter to continue"))
    elif len(option) == 10 and option[1:9].isdigit() and option[0] == "-" and option[9].upper().isalpha() \
            and option[1:10].upper() in datos.players:
        datos.game.remove(option.lstrip("-").upper())
        showPlayersGame()
    elif option == "sh":
        showPlayersGame()
    elif option == "-1":
        return option
    else:
        print("Invalid option".center(140,"*"))
        input(center_string("Enter to continue"))

def showPlayersGame():
    player_data = ""
    print("Actual players in game".center(140,"*")+"\n")
    if len(datos.game) == 0:
        print(center_string("There are no players in game"))
        input(center_string("Enter to continue"))
    else:
        for dni in datos.game:
            player_data += "".ljust(40)+dni.ljust(20) + datos.players[dni]["name"].ljust(20)
            if datos.players[dni]["human"]:
                player_data += "Human".ljust(20)
            else:
                player_data += "Bot".ljust(20)
            if datos.players[dni]["type"] == 30:
                player_data += "Cautious".ljust(20)
            elif datos.players[dni]["type"] == 40:
                player_data += "Moderated".ljust(20)
            elif datos.players[dni]["type"] == 50:
                player_data += "Bold".ljust(20)
            player_data += "\n"
        print(player_data)
        input(center_string("Enter to continue"))

def setMaxRounds():
    while True:
        try:
            datos.maxRounds = input(center_string("Max Rounds: "))
            if not datos.maxRounds.lstrip("-").isdigit():
                raise ValueError(center_string("Please, enter a number"))
            elif int(datos.maxRounds) < 1:
                raise ValueError(center_string("Please, enter a valid number of rounds"))
            else:
                datos.maxRounds = int(datos.maxRounds)
                print(center_string("Rounds set to {}".format(datos.maxRounds)))
                return datos.maxRounds
        except ValueError as e:
            print(e)
            input(center_string("Enter to continue"))

def setCardsDeck():
    for ids in datos.cartas:
        datos.mazo += [ids]
    return datos.mazo










