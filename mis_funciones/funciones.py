from . import datos
import random

def center_string(string, width=140):
    spaces = (width - len(string)) // 2
    centered_string = " " * spaces + string + " " * spaces
    return centered_string


def clear():
    print("\033[H\033[J", end="")


def playGame():
    resetPoints()
    setGamePriority(datos.mazo)
    orderAllPlayers()
    for i in range(datos.maxRounds):
        setBets()
        for dni in datos.game:
            if datos.players[dni]["human"]:
                humanRound(dni,datos.mazo)
                printStats()
            else:
                standardRound(dni, datos.mazo)
                printStats()
        clear()
        distributionPointAndNewBankCandidates()
        checkMinimum2PlayersWithPoints()
        orderAllPlayers()
        datos.maxRounds -= 1
    printWinner()
    datos.maxRounds = 5
    datos.flg_03 = False
    datos.flg_00 = True
    return

def setGamePriority(mazo):
    random.shuffle(mazo)
    datos.eliminadas = []
    for dni in datos.game:
        datos.players[dni]["initialCard"] += mazo[0]
        datos.players[dni]["roundPoints"] = datos.cartas[datos.context_game["mazo"]][mazo[0]]["realValue"]
        datos.eliminadas.append(mazo[0])
        mazo.remove(mazo[0])
    for cards in datos.cartas[datos.context_game["mazo"]]:
        if cards not in mazo:
            mazo.append(cards)
    for i in range(len(datos.game)-1):
        for j in range(len(datos.game)-i-1):
            if datos.players[datos.game[j]]["roundPoints"] == datos.players[datos.game[j+1]]["roundPoints"]:
                if datos.cartas[datos.context_game["mazo"]][datos.players[datos.game[j]]["initialCard"]]["priority"] >\
                   datos.cartas[datos.context_game["mazo"]][datos.players[datos.game[j+1]]["initialCard"]]["priority"]\
                   and datos.cartas[datos.context_game["mazo"]][datos.players[datos.game[j]]["initialCard"]]["value"] >\
                   datos.cartas[datos.context_game["mazo"]][datos.players[datos.game[j+1]]["initialCard"]]["value"]:
                    aux = datos.game[j]
                    datos.game[j] = datos.game[j+1]
                    datos.game[j+1] = aux
                elif datos.cartas[datos.context_game["mazo"]][datos.players[datos.game[j]]["initialCard"]]["priority"]>\
                     datos.cartas[datos.context_game["mazo"]][datos.players[datos.game[j+1]]["initialCard"]]["priority"]:
                    aux = datos.game[j]
                    datos.game[j] = datos.game[j+1]
                    datos.game[j+1] = aux
            elif datos.players[datos.game[j]]["roundPoints"] > datos.players[datos.game[j+1]]["roundPoints"]:
                aux = datos.game[j]
                datos.game[j] = datos.game[j+1]
                datos.game[j+1] = aux
    for i in range(len(datos.game)):
        datos.players[datos.game[i]]["priority"] = i + 1
        if datos.players[datos.game[i]]["priority"] == len(datos.game):
            datos.players[datos.game[i]]["bank"] = True
        print(datos.players[datos.game[i]])
        datos.players[datos.game[i]]["roundPoints"] = 0
        random.shuffle(mazo)

def resetPoints():
    for dni in datos.game:
        datos.players[dni]["points"] = 20
        datos.players[dni]["initialCard"] = ""
        datos.players[dni]["bank"] = False

def checkMinimum2PlayersWithPoints():
    two_players = len(datos.game)
    for dni in datos.game:
        if datos.players[dni]["points"] == 0:
            two_players -= 1
    if two_players < 2:
        print("Not enough players with points")

def orderAllPlayers(order="asc"):
    for i in range(len(datos.game)-1):
        for j in range(len(datos.game)-i-1):
            if order == "asc":
                if datos.players[datos.game[j]]["priority"] > datos.players[datos.game[j+1]]["priority"]:
                    aux = datos.game[j]
                    datos.game[j] = datos.game[j+1]
                    datos.game[j+1] = aux
            elif order == "des":
                if datos.players[datos.game[j]]["priority"] < datos.players[datos.game[j+1]]["priority"]:
                    aux = datos.game[j]
                    datos.game[j] = datos.game[j+1]
                    datos.game[j+1] = aux

def setBets():
    for dni in datos.game:
        datos.players[dni]["bet"] = 0
        if datos.players[dni]["points"] > 3:
            if datos.players[dni]["type"] == 30:
                datos.players[dni]["bet"] = int(datos.players[dni]["points"] * 0.3)
            elif datos.players[dni]["type"] == 40:
                datos.players[dni]["bet"] = int(datos.players[dni]["points"] * 0.4)
            elif datos.players[dni]["type"] == 50:
                datos.players[dni]["bet"] = int(datos.players[dni]["points"] * 0.5)
        elif datos.players[dni]["points"] <= 3:
            datos.players[dni]["bet"] = 1
        if datos.bank_player != "":
            if datos.players[dni]["bet"] > datos.players[datos.bank_player]["points"]:
                print(datos.bank_player)
                print("se activa condicion apuestas",datos.players[dni]["bet"],datos.players[datos.bank_player]["points"])
                datos.players[dni]["bet"] = datos.players[datos.bank_player]["points"]
                print("despues de igualar puntos", datos.players[dni]["bet"],
                      datos.players[datos.bank_player]["points"])
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


def standardRound(id,mazo):
    clear()
    print(datos.titulo_03)
    print("Round {}, Turn of {}".format(datos.ronda, datos.players[id]["name"]).center(140, "*"))
    higher_score = 0
    if datos.players[id]["bank"]:
        datos.bank_player = id
    if datos.players[id]["roundPoints"] > 7.5:
        return
    else:
        datos.players[id]["cards"].append(mazo[0])
        datos.players[id]["roundPoints"] += datos.cartas[datos.context_game["mazo"]][mazo[0]]["realValue"]
        datos.eliminadas.append(mazo[0])
        mazo.remove(mazo[0])
        if datos.players[id]["roundPoints"] == 7.5:
            return
        elif datos.players[id]["roundPoints"] != 7.5:
            bad_cards = 0
            plantarse = 0
            for cards in mazo:
                if datos.players[id]["roundPoints"] + datos.cartas[datos.context_game["mazo"]][cards]["realValue"] > 7.5:
                    bad_cards += 1
            if bad_cards > 0:
                plantarse = (bad_cards / len(mazo)) * 100
            if plantarse > datos.players[id]["type"] or datos.players[id]["roundPoints"] > 7.5:
                return
            elif datos.players[id]["roundPoints"] < 7.5:
                if datos.players[id]["bank"]:
                    for dni in datos.game:
                        if (datos.players[id]["roundPoints"] > datos.players[dni]["roundPoints"] and \
                                datos.players[dni]["roundPoints"] < 7.5) or (datos.players[dni]["roundPoints"] > 7.5):
                            higher_score += 1
                            half_players = len(datos.game)//2
                            if higher_score >= half_players:
                                return
                            elif higher_score <= 1 and plantarse > datos.players[id]["type"]:
                                continue
                standardRound(id,mazo)


def printWinner():
    winner = ""
    if len(datos.game) == 1:
        winner = datos.game[0]
    else:
        for i in range(len(datos.game)-1):
            for j in range(len(datos.game)-i-1):
                if datos.players[datos.game[j]]["points"] < datos.players[datos.game[j+1]]["points"]:
                    aux = datos.game[j]
                    datos.game[j] = datos.game[j+1]
                    datos.game[j+1] = aux
                    winner = datos.game[j]
    print(center_string("The winner is {} - {}, "
                        "in {} rounds, with {} points").format(winner,
                                                               datos.players[winner]["name"],
                                                               datos.ronda,
                                                               datos.players[winner]["points"]))
    input(center_string("Enter to Continue"))


def distributionPointAndNewBankCandidates():
    orderAllPlayers("des")
    for cards in datos.eliminadas:
        if cards not in datos.mazo:
            datos.mazo.append(cards)
    random.shuffle(datos.mazo)
    candidates = []
    winner = ""
    losers = []
    results = ""
    for dni in datos.game:
        if datos.players[dni]["roundPoints"] == 7.5:
            if datos.players[dni]["bank"]:
                candidates.append(dni)
                winner = candidates[0]
            elif not datos.players[dni]["bank"]:
                candidates.append(dni)
        elif datos.players[dni]["roundPoints"] < 7.5:
            candidates.append(dni)
    if len(candidates) > 1:
        for i in range(len(candidates)-1):
            for j in range(len(candidates)-i-1):
                if datos.players[candidates[j]]["roundPoints"] < datos.players[candidates[j+1]]["roundPoints"]:
                    aux = candidates[j]
                    candidates[j] = candidates[j+1]
                    candidates[j+1] = aux
                    winner = candidates[0]
                elif datos.players[candidates[j]]["roundPoints"] == datos.players[candidates[j+1]]["roundPoints"]:
                    if datos.players[candidates[j]]["priority"] < datos.players[candidates[j+1]]["priority"]:
                        aux = candidates[j]
                        candidates[j] = candidates[j+1]
                        candidates[j+1] = aux
                        winner = candidates[0]
                    else:
                        winner = candidates[0]
                else:
                    winner = candidates[0]
    else:
        winner = candidates[0]
    for dni in datos.game[::-1]:
        if not datos.players[dni]["bank"]:
            if datos.players[dni]["points"] > 0:
                if (datos.players[datos.bank_player]["roundPoints"] >= datos.players[dni]["roundPoints"] and \
                    datos.players[datos.bank_player]["roundPoints"] <= 7.5) or \
                        (datos.players[dni]["roundPoints"] > 7.5 and
                         datos.players[datos.bank_player]["roundPoints"] <= 7.5) or \
                        (datos.players[dni]["roundPoints"] == 7.5 and
                        datos.players[datos.bank_player]["roundPoints"] == 7.5):
                    if datos.players[dni]["points"] - datos.players[dni]["bet"] < 0:
                        datos.players[datos.bank_player]["points"] += datos.players[dni]["points"]
                        results += datos.space+"{} loses to bank "\
                                   "player {} and pays {}\n".format(datos.players[dni]["name"],
                                                                  datos.players[datos.bank_player]["name"],
                                                                  datos.players[dni]["points"])
                        datos.players[dni]["points"] -= datos.players[dni]["points"]
                    else:
                        datos.players[dni]["points"] -= datos.players[dni]["bet"]
                        datos.players[datos.bank_player]["points"] += datos.players[dni]["bet"]
                        results += datos.space+"{} loses to bank "\
                                   "player {} and pays {}\n".format(datos.players[dni]["name"],
                                                                  datos.players[datos.bank_player]["name"],
                                                                  datos.players[dni]["bet"])
        elif datos.players[dni]["bank"]:
            if datos.players[dni]["points"] > 0:
                if datos.players[winner]["roundPoints"] == 7.5:
                    if datos.bank_player not in winner:
                        if datos.players[datos.bank_player]["points"] - datos.players[winner]["bet"] * 2 < 0:
                            datos.players[winner]["points"] += datos.players[datos.bank_player]["points"]
                            datos.players[datos.bank_player]["points"] -= datos.players[datos.bank_player]["points"]
                        else:
                            results += datos.space+"{} pays {} " \
                                                   "points to {}\n".format(datos.players[datos.bank_player]["name"],
                                                                           datos.players[winner]["bet"] * 2,
                                                                           datos.players[winner]["name"])
                            datos.players[winner]["points"] += datos.players[winner]["bet"] * 2
                            datos.players[datos.bank_player]["points"] -= datos.players[winner]["bet"] * 2
                        datos.change = True
                for i in range(len(datos.game)):
                    if (datos.players[dni]["roundPoints"] < datos.players[datos.game[i]]["roundPoints"] and \
                        datos.players[datos.game[i]]["roundPoints"] < 7.5) or \
                            (datos.players[dni]["roundPoints"] > 7.5
                             and datos.players[datos.game[i]]["roundPoints"] < 7.5):
                        if datos.players[dni]["points"] - datos.players[datos.game[i]]["bet"] < 0:
                            datos.players[datos.game[i]]["points"] += datos.players[dni]["points"]
                            results += datos.space+"Bank player {} pays {} to {}\n".format(datos.players[dni]["name"],
                                                                             datos.players[dni]["points"],
                                                                             datos.players[datos.game[i]]["name"])
                            datos.players[dni]["points"] -= datos.players[dni]["points"]
                        else:
                            datos.players[dni]["points"] -= datos.players[datos.game[i]]["bet"]
                            datos.players[datos.game[i]]["points"] += datos.players[datos.game[i]]["bet"]
                            results += datos.space+"Bank player {} pays {} to {}\n".format(datos.players[dni]["name"],
                                                                             datos.players[datos.game[i]]["bet"],
                                                                             datos.players[datos.game[i]]["name"])
    for dni in datos.game:
        if datos.players[dni]["points"] <= 0:
            losers.append(dni)
            if datos.players[dni]["bank"] and datos.players[winner]["roundPoints"] != 7.5:
                for i in range(len(datos.game)):
                    if datos.players[datos.game[i]]["priority"] == len(datos.game) - 1:
                        results += datos.space+"Player {} is now " \
                                               "the bank\n".format(datos.players[datos.game[i]]["name"])
                        datos.players[datos.game[i]]["bank"] = True
    if datos.change:
        datos.players[datos.bank_player]["priority"] = datos.players[winner]["priority"]
        datos.players[winner]["priority"] = len(datos.game)
        orderAllPlayers("des")
        datos.players[datos.bank_player]["bank"] = False
        datos.players[winner]["bank"] = True
        datos.bank_player = winner
        results += datos.space+"Player with 7.5 points {} is now the bank\n".format(datos.players[winner]["name"])
    for i in range(len(losers)):
        datos.game.remove(losers[i])
        results += datos.space+"{} is out of the game!".format(datos.players[losers[i]]["name"])
    datos.players[datos.bank_player]["priority"] = len(datos.game)
    for i in range(len(datos.game)):
        if datos.players[datos.game[i]]["priority"] != 1:
            datos.players[datos.game[i]]["priority"] = datos.players[datos.bank_player]["priority"] - i
    print(datos.titulo_03)
    print("Round is over, these are the results".center(140, "*"))
    print(results)
    printStats()
    for dni in datos.game:
        datos.players[dni]["roundPoints"] = 0
        datos.players[dni]["cards"] = []
    datos.change = False
    datos.ronda += 1


def humanRound(id,mazo):
    clear()
    print(datos.titulo_03)
    print("Round {}, Turn of {}".format(datos.ronda, datos.players[id]["name"]).center(140, "*"))
    if datos.players[id]["bank"]:
        datos.bank_player = id
    textOps = (datos.space + "1)View Stats\n"+
               datos.space + "2)View Game Stats\n"+
               datos.space + "3)Set Bet\n"+
               datos.space + "4)Order Card\n"+
               datos.space + "5)Automatic Play\n"+
               datos.space + "6)Stand")
    inputOptText = datos.space + "Option: "
    range_list = [1,2,3,4,5]
    exception = [6]
    while True:
        option = getOpt(textOps, inputOptText, range_list, exception)
        if option == 1:
            printPlayerStats(id)
            clear()
            print(datos.titulo_03)
            print("Round {}, Turn of {}".format(datos.ronda, datos.players[id]["name"]).center(140, "*"))
        elif option == 2:
            clear()
            print(datos.titulo_03)
            print("Round {}, Turn of {}".format(datos.ronda, datos.players[id]["name"]).center(140, "*"))
            printStats()
        elif option == 3:
            if datos.players[id]["bank"]:
                print(center_string("You're not allowed to set a bet if you're the bank"))
                input(center_string("Enter to Continue"))
            elif len(datos.players[id]["cards"]) >= 1:
                print(center_string("You're not allowed to set your bet if you already have 1 card or more"))
                input(center_string("Enter to Continue"))
            else:
                while True:
                    try:
                        datos.players[id]["bet"] = input(datos.space+"Set your bet: ")
                        if not datos.players[id]["bet"].lstrip("-").isdigit():
                            raise ValueError("\nPlease, introduce only numbers")
                        elif int(datos.players[id]["bet"]) <= 0:
                            raise ValueError("\nBet has to be a positive number and higher than 0")
                        elif int(datos.players[id]["bet"]) > datos.players[id]["points"]:
                            raise ValueError("\nBet has to be a "
                                             "number between 1 and {}".format(datos.players[id]["points"]))
                        else:
                            datos.players[id]["bet"] = int(datos.players[id]["bet"])
                            print(datos.space+"Bet set to {}".format(datos.players[id]["bet"]))
                            input(center_string("Enter to continue"))
                            break
                    except ValueError as e:
                        print(e)
                        input(center_string("Enter to continue"))
        elif option == 4:
            if len(datos.players[id]["cards"]) > 0 and datos.players[id]["roundPoints"] <= 7.5:
                bad_cards = 0
                plantarse = 0
                for cards in mazo:
                    if datos.players[id]["roundPoints"] + \
                            datos.cartas[datos.context_game["mazo"]][cards]["realValue"] > 7.5:
                        bad_cards += 1
                if bad_cards > 0:
                    plantarse = (bad_cards / len(mazo)) * 100
                another_card = input(datos.space+"Chances of exceeding 7.5 are {}%\n".format(plantarse)+datos.space+
                                     "Are you sure you want to draw another card? "
                                     "(Y/y = yes, any other key = no): ")
                if not another_card.lower() == "y":
                    continue
            if datos.players[id]["roundPoints"] < 7.5:
                datos.players[id]["cards"].append(mazo[0])
                print(center_string("You draw the "
                                    "{} card".format(datos.cartas[datos.context_game["mazo"]][mazo[0]]["literal"])))
                datos.players[id]["roundPoints"] += datos.cartas[datos.context_game["mazo"]][mazo[0]]["realValue"]
                print(center_string("Now you have {} points".format(datos.players[id]["roundPoints"])))
                datos.eliminadas.append(mazo[0])
                mazo.remove(mazo[0])
                input(center_string("Enter to continue"))
            else:
                print(datos.space+"You have {} points, "
                                    "you can't draw more cards".format(datos.players[id]["roundPoints"]))
        elif option == 5:
            standardRound(id,mazo)
            return
        elif option == 6:
            clear()
            print(datos.titulo_03)
            print("Round {}, Turn of {}".format(datos.ronda, datos.players[id]["name"]).center(140, "*"))
            return
        clear()
        print(datos.titulo_03)
        print("Round {}, Turn of {}".format(datos.ronda, datos.players[id]["name"]).center(140, "*"))

def printStats():
    titulo = "="*140+"\n"+\
             "|"+"Name".center(10)+\
                  "|"+"Human".center(10)+\
                  "|"+"Priority".center(10)+\
                  "|"+"Type".center(10)+\
                  "|"+"Bank".center(10)+\
                  "|"+"Bet".center(10)+\
                  "|"+"Points".center(10)+\
                  "|"+"Roundpoints".center(15)+\
                  "|"+"Cards".center(50)+"\n"+"="*140
    playerId = ""
    for i in range(len(datos.game)):
        playerId += "|"+str(datos.players[datos.game[i]]["name"]).center(10) +"|"+\
                    str(datos.players[datos.game[i]]["human"]).center(10) +"|"+ \
                    str(datos.players[datos.game[i]]["priority"]).center(10) + "|"+\
                    str(datos.players[datos.game[i]]["type"]).center(10) +"|"+ \
                    str(datos.players[datos.game[i]]["bank"]).center(10) +"|"+ \
                    str(datos.players[datos.game[i]]["bet"]).center(10) +"|"+ \
                    str(datos.players[datos.game[i]]["points"]).center(10) + "|"+ \
                    str(datos.players[datos.game[i]]["roundPoints"]).center(15) + "|"
        for cards in datos.players[datos.game[i]]["cards"]:
            playerId += cards + " "
        playerId += "\n" + "-" * 140 + "\n"
    print(titulo)
    print(playerId)
    input(center_string("Enter to Continue"))

def printPlayerStats(id):
    clear()
    print(datos.titulo_03)
    print("Round {}, Turn of {}".format(datos.ronda,datos.players[id]["name"]).center(140,"*"))
    info = datos.space+"Name".ljust(20)+datos.players[id].get("name") + "\n" + \
           datos.space+"Human".ljust(20)+ str(datos.players[id].get("human")) + "\n"+\
           datos.space+"Type".ljust(20)+ str(datos.players[id].get("type")) + "\n" + \
           datos.space+"Bank".ljust(20)+ str(datos.players[id].get("bank")) + "\n"+ \
           datos.space+"Bet".ljust(20)+ str(datos.players[id].get("bet")) + "\n" + \
           datos.space+"Points".ljust(20)+ str(datos.players[id].get("points")) + "\n"+ \
           datos.space+"Cards".ljust(20)
    for cards in datos.players[id]["cards"]:
        info += str(cards)+";"
    info += "\n"+datos.space+"RoundPoints".ljust(20)+str(datos.players[id].get("roundPoints")) + "\n"
    print(info)
    input(center_string("Enter to continue"))





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
    option_range = [1, 2, 3]
    exception = [4]
    option = getOpt(textOpts, inputOptText, option_range, exception)
    if option == 1:
        clear()
        print(datos.titulo_021)
        showPlayersGame()
        datos.flg_02 = False
        datos.flg_021 = True
    elif option == 2:
        clear()
        setCardsDeck()
    elif option == 3:
        clear()
        setMaxRounds()
    elif option == 4:
        clear()
        datos.flg_02 = False
        datos.flg_00 = True


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
    print(datos.titulo_023)
    while True:
        try:
            datos.maxRounds = input(datos.space+"Max Rounds: ")
            if not datos.maxRounds.lstrip("-").isdigit():
                raise ValueError(center_string("Please, enter a number"))
            elif int(datos.maxRounds) < 1:
                raise ValueError(center_string("Please, enter a valid number of rounds"))
            elif int(datos.maxRounds) >= 30:
                raise ValueError(center_string("Maximum number of rounds exceeded"))
            else:
                datos.maxRounds = int(datos.maxRounds)
                print(center_string("Rounds set to {}".format(datos.maxRounds)))
                return datos.maxRounds
        except ValueError as e:
            print(e)
            input(center_string("Enter to continue"))

def setCardsDeck():
    print(datos.titulo_022)
    textOps = datos.space+"1) ESP - ESP \n"+\
              datos.space+"2) POK - POK \n"+\
              datos.space+"0) Go Back\n"
    inputOptText = datos.space + "Option: "
    range_list = [1,2]
    exception = [0]
    option = getOpt(textOps,inputOptText,range_list,exception)
    if option == 1:
        datos.context_game["mazo"] = "spanish"
        for ids in datos.cartas["spanish"]:
            datos.mazo += [ids]
        print(datos.space+"Deck set to Spanish deck")
        input(datos.space+"Enter to continue")
    elif option == 2:
        datos.context_game["mazo"] = "poker"
        for ids in datos.cartas["poker"]:
            datos.mazo += [ids]
        print(datos.space+"Deck set to Poker deck")
        input(datos.space+"Enter to continue")
    elif option == 0:
        return
    return datos.mazo










