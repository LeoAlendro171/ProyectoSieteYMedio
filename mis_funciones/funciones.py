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

