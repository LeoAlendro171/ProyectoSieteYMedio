import mysql.connector
import time
from . import datos
import random
import _mysql_connector

def prueba():
    cnx = mysql.connector.connect(user = "root", password = "1234",
                                host = "127.0.0.1",
                                database = "seven_half")
def center_string(string, width=140):
    spaces = (width - len(string)) // 2
    centered_string = " " * spaces + string + " " * spaces
    return centered_string


def getPlayers():
    cnx = mysql.connector.connect(user = "root", password = "1234",
                                  host = "127.0.0.1",
                                  database = "seven_half")
    cursor = cnx.cursor()
    cursor.execute("SELECT * from player")
    for table_name in cursor:
        if table_name[0] not in datos.players:
            if table_name[3] == 0:
                elupdate = {table_name[0]:{"name": table_name[1],"human": False,
                                           "bank": False, "initialCard": "", "priority": 0,
                                           "type": table_name[2],"bet": 0,"points": 0,
                                           "cards": [],"roundPoints": 0}}
                datos.players.update(elupdate)
            elif table_name[3] == 1:
                elupdate = {table_name[0]:{"name": table_name[1],"human": True,
                                           "bank": False, "initialCard": "", "priority": 0,
                                           "type": table_name[2],"bet": 0,"points": 0,
                                           "cards": [],"roundPoints": 0}}
                datos.players.update(elupdate)

def clear():
    print("\033[H\033[J", end="")


def roundHeader(playerId):
    print(datos.titulo_03)
    print("Round {}, Turn of {}".format(datos.ronda, datos.players[playerId]["name"]).center(140, "*"))


def playGame():
    resetPoints()
    game_id = getGameId()
    datos.cardgame["cardgame_id"] = game_id
    datos.cardgame["players"] = len(datos.game)
    datos.cardgame["start_hour"] = time.strftime("%Y-%m-%d %H:%M:%S")
    setGamePriority(datos.mazo)
    fill_player_game(datos.player_game,game_id,"starting_points")
    orderAllPlayers()
    for i in range(datos.maxRounds):
        setBets()
        for dni in datos.game:
            if datos.players[dni]["human"]:
                humanRound(dni,datos.mazo)
                roundHeader(dni)
                printStats()
            else:
                standardRound(dni, datos.mazo)
                roundHeader(dni)
                printStats()
            fill_player_game_round(datos.player_game_round,game_id,datos.ronda,"starting_round_points")
        clear()
        distributionPointAndNewBankCandidates()
        fill_player_game_round(datos.player_game_round, game_id, datos.ronda, "ending_round_points")
        for dni in datos.game:
            datos.players[dni]["roundPoints"] = 0
            datos.players[dni]["cards"] = []
        datos.ronda += 1
        checkMinimum2PlayersWithPoints()
        orderAllPlayers()
        datos.maxRounds -= 1
        if datos.maxRounds <= 0:
            break
    printWinner()
    datos.cardgame["rounds"] = datos.ronda
    datos.cardgame["end_hour"] = time.strftime("%Y-%m-%d %H:%M:%S")
    fill_player_game(datos.player_game, game_id, "ending_points")
    insertBBDDCardgame(datos.cardgame)
    insertBBDD_player_game(datos.player_game, game_id)
    insertBBDD_player_game_round(datos.player_game_round,game_id)
    datos.maxRounds = 5
    datos.ronda = 0
    datos.flg_03 = False
    datos.flg_00 = True
    return


def insertBBDDCardgame(cardgame):
    cnx = mysql.connector.connect(user = "root", password = "1234",
                                  host = "127.0.0.1",
                                  database = "seven_half")
    cursor = cnx.cursor()
    cursor.execute("INSERT INTO cardgame (cardgame_id, players, rounds, start_hour, end_hour)"\
                   "VALUES (%s, %s, %s, %s, %s)",
                   (cardgame["cardgame_id"],cardgame["players"], cardgame["rounds"],
                    cardgame["start_hour"], cardgame["end_hour"]))
    cnx.commit()

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
        print(center_string("Not enough players with points"))
        input(center_string("Enter to continue"))
        datos.maxRounds = 0
        return datos.maxRounds


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
                datos.players[dni]["bet"] = datos.players[datos.bank_player]["points"]


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
    if datos.players[id]["roundPoints"] == 0:
        roundHeader(id)
        printStats()
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
            clear()
            return
        elif datos.players[id]["roundPoints"] != 7.5:
            bad_cards = 0
            plantarse = 0
            for cards in mazo:
                if datos.players[id]["roundPoints"] + \
                        datos.cartas[datos.context_game["mazo"]][cards]["realValue"] > 7.5:
                    bad_cards += 1
            if bad_cards > 0:
                plantarse = (bad_cards / len(mazo)) * 100
            if plantarse > datos.players[id]["type"] or datos.players[id]["roundPoints"] > 7.5:
                clear()
                return
            elif datos.players[id]["roundPoints"] < 7.5:
                if datos.players[id]["bank"]:
                    for dni in datos.game:
                        if (datos.players[id]["roundPoints"] > datos.players[dni]["roundPoints"] and
                                datos.players[dni]["roundPoints"] < 7.5) or (datos.players[dni]["roundPoints"] > 7.5):
                            higher_score += 1
                            half_players = len(datos.game)//2
                            if higher_score >= half_players:
                                return
                            elif higher_score <= 1 and plantarse > datos.players[id]["type"]:
                                continue
                standardRound(id,mazo)


def printWinner():
    clear()
    print(datos.titulo_winner)
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
                elif datos.players[datos.game[j]]["points"] == datos.players[datos.game[j+1]]["points"]:
                    if datos.players[datos.game[j]]["priority"] > datos.players[datos.game[j+1]]["priority"]:
                        aux = datos.game[j]
                        datos.game[j] = datos.game[j + 1]
                        datos.game[j + 1] = aux
                winner = datos.game[j]
    print(center_string("The winner is {} - {}, "
                        "in {} rounds, with {} points").format(winner,
                                                               datos.players[winner]["name"],
                                                               datos.ronda,
                                                               datos.players[winner]["points"]))
    input(center_string("Enter to Continue"))
    clear()


def distributionPointAndNewBankCandidates():
    orderAllPlayers("des")
    for cards in datos.eliminadas:
        if cards not in datos.mazo:
            datos.mazo.append(cards)
    random.shuffle(datos.mazo)
    candidates = []
    winner = ""
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
            datos.losers.append(dni)
            if datos.players[dni]["bank"] and datos.players[winner]["roundPoints"] != 7.5:
                for i in range(len(datos.game)):
                    if datos.players[datos.game[i]]["priority"] == len(datos.game) - 1:
                        results += datos.space+"Player {} is now " \
                                               "the bank\n".format(datos.players[datos.game[i]]["name"])
                        datos.players[datos.game[i]]["bank"] = True
                        datos.bank_player = datos.game[i]
    if datos.change:
        datos.players[datos.bank_player]["priority"] = datos.players[winner]["priority"]
        datos.players[winner]["priority"] = len(datos.game)
        orderAllPlayers("des")
        datos.players[datos.bank_player]["bank"] = False
        datos.players[winner]["bank"] = True
        datos.bank_player = winner
        results += datos.space+"Player with 7.5 points {} is now the bank\n".format(datos.players[winner]["name"])
    for i in range(len(datos.losers)):
        datos.game.remove(datos.losers[i])
        results += datos.space+"{} is out of the game!".format(datos.players[datos.losers[i]]["name"])
    datos.losers = []
    datos.players[datos.bank_player]["priority"] = len(datos.game)
    for i in range(len(datos.game)):
        if datos.players[datos.game[i]]["priority"] != 1:
            datos.players[datos.game[i]]["priority"] = datos.players[datos.bank_player]["priority"] - i
    clear()
    print(datos.titulo_03)
    print("Round is over, these are the results".center(140, "*"))
    print(results)
    printStats()
    datos.change = False


def humanRound(id,mazo):
    clear()
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
        clear()
        roundHeader(id)
        option = getOpt(textOps, inputOptText, range_list, exception)
        if option == 1:
            printPlayerStats(id)
            clear()
        elif option == 2:
            clear()
            roundHeader(id)
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
            return


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
    roundHeader(id)
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


def randomNIF():
    nif = ""
    for i in range(8):
        nif += str(random.randint(0, 9))
    if int(nif) % 23 in range(len(datos.letrasDni)):
        nif += datos.letrasDni[int(nif) % 23]
        if nif not in datos.players:
            return nif
        else:
            randomNIF()


def setNewPlayer(human = True):
    while True:
        try:
            print(datos.titulo_011)
            notbot = 0
            name = input(datos.space+"Name: ")
            if not name.isalpha():
                raise ValueError(datos.space + "Incorrect name, enter a name that is not empty with only letters")
            if human:
                notbot = 1
                dni = input(datos.space+"NIF: ")
                if not len(dni) == 9 or not dni[:8].isdigit() or not dni[8].isalpha() \
                   or not datos.letrasDni[int(dni[:8])%23] == dni[8].upper():
                    raise ValueError(datos.space + "Wrong NIF")
                elif dni in datos.players:
                    raise ValueError(datos.space + "NIF {} already exists".format(dni))
            elif not human:
                dni = randomNIF()
            textOps = datos.space+"Select your Profile:\n"+\
                      datos.space+"1)Cautious\n"+\
                      datos.space+"2)Moderated\n"+\
                      datos.space+"3)Bold\n"
            inputOptText = datos.space+"Option: "
            option_range = [1,2,3]
            exception = []
            option = getOpt(textOps,inputOptText,option_range,exception)
            profile = 0
            if option == 1:
                profile = 30
            elif option == 2:
                profile = 40
            elif option == 3:
                profile = 50
            info = datos.space+"Name:".ljust(10) + name +"\n"+\
                   datos.space+"DNI:".ljust(10) + dni +"\n"
            if profile == 30:
                info += datos.space+"Profile:".ljust(10) + "Cautious"+"\n"
            elif profile == 40:
                info += datos.space+"Profile:".ljust(10) + "Moderated"+"\n"
            elif profile == 50:
                info += datos.space+"Profile:".ljust(10) + "Bold"+"\n"
            print(info)
            confirmation = input(datos.space+"Is it okay? (Y/y = yes, any other key = no): ")
            if not confirmation.lower() == "y":
                return
            else:
                cnx = mysql.connector.connect(user="root", password="1234",
                                              host="127.0.0.1",
                                              database="seven_half")
                cursor = cnx.cursor()
                cursor.execute("INSERT INTO player (player_id, player_name, player_risk,human) "
                               "VALUES ('{}','{}',{},{})".format(dni,name,profile,notbot))
                cnx.commit()
                getPlayers()
                print(center_string("New player added to the BBDD"))
                input(center_string("Enter to continue"))
                return


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


def removeBBDDPlayer():
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
    while True:
        try:
            option = input(datos.space+"Option (-id to remove player, -1 to exit): ")
            if option == "-1":
                return
            elif option[0] != "-":
                raise ValueError(datos.space+"Invalid Option")
            elif option.lstrip("-") not in datos.players:
                raise ValueError(datos.space+"Invalid Option")
            else:
                cnx = mysql.connector.connect(user="root", password="1234",
                                              host="127.0.0.1",
                                              database="seven_half")
                cursor = cnx.cursor()
                cursor.execute("DELETE from player WHERE player_id = '{}'".format(option.lstrip("-")))
                cnx.commit()
                datos.players.pop(option.lstrip("-"))
                getPlayers()
                print(center_string("Player {} removed from the BBDD".format(option.lstrip("-"))))
                input(center_string("Enter to continue"))
                clear()
                removeBBDDPlayer()
        except ValueError as e:
            print(e)


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
                input(center_string("Enter to continue"))
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


def fill_player_game(player_game,gameID,fields):
    player_game[gameID] = {}
    if player_game[gameID] == {}:
        for i in range(len(datos.game)):
            player_dict = {datos.game[i]: {"initial_card_id": datos.players[datos.game[i]]["initialCard"],
                                            "initial_card_deck_id": "",
                                            "starting_points": 20, "ending_points": 0}}
            player_game[gameID].update(player_dict)
    for dni in player_game[gameID]:
        if datos.context_game["mazo"] == "spanish":
            player_game[gameID][dni] = {"initial_card_id": datos.players[dni]["initialCard"],
                                        "initial_card_deck_id": "ESP",
                                        "starting_points": 20, "ending_points": 0}
        elif datos.context_game["mazo"] == "poker":
            player_game[gameID][dni] = {"initial_card_id": datos.players[dni]["initialCard"],
                                        "initial_card_deck_id": "POK",
                                        "starting_points": 20, "ending_points": 0}
        player_game[gameID][dni][fields] = datos.players[dni]["points"]


def insertBBDD_player_game(player_game,cardgame_id):
    cnx = mysql.connector.connect(user = "root", password = "1234",
                                  host = "127.0.0.1",
                                  database = "seven_half")
    cursor = cnx.cursor()
    for dni in player_game[cardgame_id]:
        cursor.execute("INSERT INTO player_game (cardgame_id, player_id, initial_card_id, initial_card_deck_id,"
                       "starting_points, ending_points) VALUES (%s, %s, %s, %s, %s, %s)",
                       (cardgame_id, dni, player_game[cardgame_id][dni]["initial_card_id"],
                        player_game[cardgame_id][dni]["initial_card_deck_id"],
                        player_game[cardgame_id][dni]["starting_points"],
                        player_game[cardgame_id][dni]["ending_points"]))
        cnx.commit()


def fill_player_game_round(player_game_round,gameID,round,fields):
    if player_game_round == {}:
        player_game_round[gameID] = {}
        if player_game_round[gameID] == {}:
            player_game_round[gameID][round] = {}
    elif round not in player_game_round[gameID]:
        next_round = {round:{}}
        player_game_round[gameID].update(next_round)
    if len(player_game_round[gameID][round]) == 0:
        for i in range(len(datos.game)):
            round_dict = {datos.game[i]: {"is_bank": 0, "bet_points": 0, "cards_value": 0,
                                                          "starting_round_points": 0, "ending_round_points": 0}}
            player_game_round[gameID][round].update(round_dict)
    for dni in player_game_round[gameID][round]:
        if datos.players[dni]["bank"]:
            player_game_round[gameID][round][dni]["is_bank"] = 1
        player_game_round[gameID][round][dni]["bet_points"] = datos.players[dni]["bet"]
        player_game_round[gameID][round][dni]["cards_value"] = datos.players[dni]["roundPoints"]
        player_game_round[gameID][round][dni][fields] = datos.players[dni]["points"]


def insertBBDD_player_game_round(player_game_round,cardgame_id):
    cnx = mysql.connector.connect(user = "root", password = "1234",
                                  host = "127.0.0.1",
                                  database = "seven_half")
    cursor = cnx.cursor()
    for rounds in player_game_round[cardgame_id]:
        for dni in player_game_round[cardgame_id][rounds]:
            cursor.execute("INSERT INTO player_game_round "
                           "(cardgame_id, round_num, player_id, is_bank, bet_points, cards_value,"
                           "starting_round_points, ending_round_points) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                           (cardgame_id, rounds, dni, player_game_round[cardgame_id][rounds][dni]["is_bank"],
                            player_game_round[cardgame_id][rounds][dni]["bet_points"],
                            player_game_round[cardgame_id][rounds][dni]["cards_value"],
                            player_game_round[cardgame_id][rounds][dni]["starting_round_points"],
                            player_game_round[cardgame_id][rounds][dni]["ending_round_points"]))
            cnx.commit()


def getBBDDRanking():
    dict_datos = {}
    cnx = mysql.connector.connect(user="root", password="1234",
                                  host="127.0.0.1",
                                  database="seven_half")
    cursor = cnx.cursor()
    cursor.execute("drop view if exists ranking")
    cnx.commit()
    st_ranking = "create view ranking as select pg.player_id AS player_id, " \
            "sum((pg.ending_points - pg.starting_points)) AS earnings, count(pg.cardgame_id) AS games_played, " \
            "sum(timestampdiff(SECOND,c.start_hour,c.end_hour)) / 60 AS minutes_played from player_game pg " \
            "join cardgame c on pg.cardgame_id = c.cardgame_id group by pg.player_id"
    cursor = cnx.cursor()
    cursor.execute(st_ranking)
    cnx.commit()
    cursor.execute("SELECT * FROM ranking")
    info = cursor.fetchall()
    for player in info:
        dict_datos[player[0]]={}
        dict_datos[player[0]]["earnings"] = int(player[1])
        dict_datos[player[0]]["games_played"] = int(player[2])
        dict_datos[player[0]]["minutes_played"] = float(player[3])
    return dict_datos


def ranking():
    textOpts = datos.space + "1)Players With More Earnings" + "\n" + \
               datos.space + "2)Players With More Games Played"+"\n" + \
               datos.space + "3)Players With More Minutes Played" + "\n" + \
               datos.space + "4)Go Back"
    inputOptText = datos.space + "Option: "
    option_range = [1, 2, 3]
    exception = [4]
    option = getOpt(textOpts, inputOptText, option_range, exception)
    clear()
    if option == 1:
        print(datos.titulo_earnings)
        returnListRanking()
    elif option == 2:
        print(datos.titulo_games_played)
        returnListRanking("games_played")
    elif option == 3:
        print(datos.titulo_minutes_played)
        returnListRanking("minutes_played")
    elif option == 4:
        clear()
        datos.flg_04 = False
        datos.flg_00 = True


def getGameId():
    cnx = mysql.connector.connect(user="root", password="1234",
                                  host="127.0.0.1",
                                  database="seven_half")
    cursor = cnx.cursor()
    cursor.execute("SELECT cardgame_id from cardgame")
    id_game = 0
    for ids in cursor:
        for values in ids:
            id_game = values + 1
    return id_game


def returnListRanking(field="earnings"):
    dict_datos = getBBDDRanking()
    players = []
    for dni in dict_datos:
        players.append(dni)
    for i in range(len(players) - 1):
        for j in range(len(players) - i - 1):
            if dict_datos[players[j]][field] < dict_datos[players[j + 1]][field]:
                aux = players[j]
                players[j] = players[j + 1]
                players[j + 1] = aux
    info = ""
    header = center_string("TOP TEN PLAYERS") + "\n" + \
             datos.space + "-" * 45 + "\n" + \
             datos.space + "Player ID".ljust(15)
    if field == "earnings":
        header += "Name".ljust(20)+"Earnings".ljust(10) + "\n"
    elif field == "games_played":
        header += "Name".ljust(18)+"Games Played".ljust(10) + "\n"
    elif field == "minutes_played":
        header += "Name".ljust(16)+"Minutes Played".ljust(10) + "\n"
    header += datos.space + "-" * 45
    for i in range(len(players)):
        info += datos.space + players[i].ljust(15) + \
                datos.players[players[i]]["name"].ljust(20) + \
                str(dict_datos[players[i]][field]).center(8) + "\n"
        if i == 9:
            break
    print(header)
    print(info)
    input(center_string("Enter to continue"))
    clear()


def reports():
    cnx = mysql.connector.connect(user="root", password="1234",
                                  host="127.0.0.1",
                                  database="seven_half")
    textOpts = datos.space + "1)Initial card more repeated by each user,\n" + datos.space + \
               "only users who have played a minimum of 3 games" \
               + "\n" + datos.space + "2)Player who makes the highest bet per game,\n" + datos.space + \
               "find the round with the highest bet" + \
               "\n" + datos.space + "3)Player who makes the lowest bet per game" \
               + "\n" + datos.space + "4)Percentage of rounds won per player in each game\n" + datos.space + "(%)," \
                                    "as well as their average bet for the game" \
               + "\n" + datos.space + "5)List of games won by Bots" \
               + "\n" + datos.space + "6)Rounds won by the bank in each game" \
               + "\n" + datos.space + "7)Number of users that have been the bank in each game" \
               + "\n" + datos.space + "8)Average bet per game" \
               + "\n" + datos.space + "9)Average bet of the first round of each game" \
               + "\n" + datos.space + "10)Average bet of the last round of each game" \
               + "\n" + datos.space + "11)Go back"
    inputOptText = datos.space + "Option: "
    option_range = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    exception = [11]
    option = getOpt(textOpts, inputOptText, option_range, exception)
    dict_datos = {}
    keys = []
    if option == 1:
        highest_bet = "select * " \
                 + "from (select p.cardgame_id,p.player_id,max(p.bet_points) as max_bet from player_game_round p " \
                 + "where p.bet_points is not null group by 1,2) pb where pb.max_bet = (select max(p1.bet_points) from "\
                 + "player_game_round p1 where p1.cardgame_id=pb.cardgame_id);"
        cursor = cnx.cursor()
        cursor.execute(highest_bet)
        info = cursor.fetchall()
        for cardgame in info:
            dict_datos[cardgame[0]] = {}
            dict_datos[cardgame[0]]["player_id"] = cardgame[1]
            dict_datos[cardgame[0]]["max_bet"] = int(cardgame[2])
        print(dict_datos)
    elif option == 2:
        bank_players = "select p.cardgame_id,count(distinct player_id) as bancas from player_game_round p "\
                     + "where p.is_bank is true group by 1;"
        cursor = cnx.cursor()
        cursor.execute(bank_players)
        info = cursor.fetchall()
        for cardgame in info:
            dict_datos[cardgame[0]] = {}
            dict_datos[cardgame[0]]["bancas"] = cardgame[1]
        header = datos.space+"-"*45+"\n"+\
                 datos.space+"Cardgame".center(20) + \
                 "Bank Players".center(30)+"\n"+\
                 datos.space+"-"*45
        info = ""
        for cardgame in dict_datos:
            keys.append(cardgame)
        contador = 1
        for i in range(len(keys)):
            clear()
            print(datos.titulo_05)
            print(header)
            contador += 1
            info += datos.space+str(keys[i]).center(20) + str(dict_datos[keys[i]]["bancas"]).center(30) + "\n"
            if contador == 10:
                print(info)
                info = ""
                keep_going = input(datos.space+"+ to show more, any other key to stop: ")
                if keep_going != "+":
                    break
                else:
                    contador = 1
        input(center_string("Enter to continue"))
    if option == 11:
        clear()
        datos.flg_05 = False
        datos.flg_00 = True











