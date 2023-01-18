from mis_funciones import funciones
from mis_funciones import datos


while not datos.Salir:
    while datos.flg_00:
        print(datos.titulo_00)
        textOpts = datos.space + "1)Add/Remove/Show Players" + "\n" + datos.space + "2)Settings" + \
                "\n" + datos.space + "3)Play Game" + "\n" + datos.space + "4)Ranking" + "\n" + datos.space + \
                "5)Reports" + "\n" + datos.space + "6)Exit"
        inputOptText = datos.space + "Option: "
        option_range = [1,2,3,4,5]
        exception = [6]
        option = funciones.getOpt(textOpts,inputOptText,option_range,exception)
        if option == 1:
            datos.flg_00 = False
            datos.flg_01 = True
        elif option == 2:
            datos.flg_00 = False
            datos.flg_02 = True
        elif option == 3:
            if len(datos.game) < 2:
                print(datos.space + "Set the players that compose the game first")
                input(datos.space + "Enter to continue")
                funciones.clear()
            elif len(datos.mazo) == 0:
                print(datos.space + "Set the deck first")
                input(datos.space + "Enter to continue")
                funciones.clear()
            elif datos.maxRounds == 0:
                print(funciones.center_string("Please, set the number of rounds first"))
                funciones.clear()
            else:
                funciones.playGame()
        elif option == 4:
            datos.flg_00 = False
            datos.flg_04 = True
        elif option == 5:
            datos.flg_00 = False
            datos.flg_05 = True
        elif option == 6:
            datos.flg_00 = False
            datos.Salir = True
    while datos.flg_01:
        funciones.clear()
        print(datos.titulo_01)
        option = funciones.addRemovePlayers()
        if option == 1:
            funciones.clear()
            funciones.setNewPlayer()
        elif option == 4:
            funciones.clear()
            datos.flg_01 = False
            datos.flg_00 = True
    while datos.flg_02:
        funciones.clear()
        print(datos.titulo_02)
        funciones.settings()
    while datos.flg_021:
        print(datos.titulo_021)
        option = funciones.setPlayersGame()
        if option == "-1":
            datos.flg_021 = False
            datos.flg_02 = True
    while datos.flg_04:
        funciones.clear()
        print(datos.titulo_04)
        textOpts = datos.space + "1)Players With More Earnings" + "\n" + datos.space + "2)Players With More Games Played" + \
                   "\n" + datos.space + "3)Players With More Minutes Played" + "\n" + datos.space + "4)Go Back"
        inputOptText = datos.space + "Option: "
        option_range = [1, 2, 3, 4]
        exception = [5]
        option = funciones.getOpt(textOpts, inputOptText, option_range, exception)
        if option == 4:
            funciones.clear()
            datos.flg_04 = False
            datos.flg_00 = True
    while datos.flg_05:
        funciones.clear()
        print(datos.titulo_05)
        textOpts = datos.space + "1)Initial card more repeated by each user,\n" + datos.space + \
                   "only users who have played a minimum of 3 games"\
                   + "\n" + datos.space + "2)Player who makes the highest bet per game,\n" + datos.space + \
                   "find the round with the highest bet" +\
                   "\n" + datos.space + "3)Player who makes the lowest bet per game"\
                   + "\n" + datos.space + "4)Percentage of rounds won per player in each game\n" + datos.space + " (%), " \
                         "as well as their average bet for the game"\
                   + "\n" + datos.space + "5)List of games won by Bots"\
                   + "\n" + datos.space + "6)Rounds won by the bank in each game"\
                   + "\n" + datos.space + "7)Number of users that have been the bank in each game"\
                   + "\n" + datos.space + "8)Average bet per game"\
                   + "\n" + datos.space + "9)Average bet of the first round of each game"\
                   + "\n" + datos.space + "10)Average bet of the last round of each game"\
                   + "\n" + datos.space + "11)Go back"
        inputOptText = datos.space + "Option: "
        option_range = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        exception = [11]
        option = funciones.getOpt(textOpts, inputOptText, option_range, exception)
        if option == 11:
            funciones.clear()
            datos.flg_05 = False
            datos.flg_00 = True
