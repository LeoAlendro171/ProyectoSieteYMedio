from . import datos
def clear():
    print("\033[H\033[J", end="")

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
            input(" "*58+"Press enter to continue")

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
    exception = [5]
    option = getOpt(textOpts, inputOptText, option_range, exception)
    if option == 1:
        print("Actual players in game".center(140,"*"))
        if len(datos.game) == 0:
            print(datos.space+"There are no players in game")
            input(datos.space+"Enter to continue")
        return option
    elif option == 4:
        return option


def setPlayersGame():
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
    input("Enter to continue")





