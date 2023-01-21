from mis_funciones import funciones
from mis_funciones import datos


while not datos.Salir:
    funciones.getPlayers()
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
            elif datos.maxRounds <= 0:
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
        elif option == 2:
            funciones.clear()
            funciones.setNewPlayer(False)
        elif option == 3:
            funciones.clear()
            funciones.removeBBDDPlayer()
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
        funciones.ranking()
    while datos.flg_05:
        funciones.clear()
        print(datos.titulo_05)
        funciones.reports()
