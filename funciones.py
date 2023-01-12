import datos as d
import datos_pruebas as dp
import random



'''def setGamePriority(mazo):
    #Por cada dni en la lista de jugadores de la partida, atribuye una carta.
    list_value = {}
    for dni in d.game:
        #Extraemos el len del mazo
        len_mazo = len(mazo)
        #Atribuimos a cada uno de los dni una carta de borma aleatoria entre la posicion 0 y la posicion final del mazo.
        d.players[dni]["initialcard"] = mazo[random.randint(0,len_mazo)]
        #Eliminamos del mazo la carta que hemos entregado.
        mazo.remove(d.players[dni]["initialcard"])
    
    for dni in d.game:

        list_value[d.cartas[d.players[dni]["initialcard"]]] =  d.cartas[d.players[dni]["initialcard"]]["value"]

    for carta in list_value:

        contaje = list_value.count(carta)

        if contaje > 1:

            for dni in list_value:
                list_value[d.cartas[d.players[dni]["initialcard"]]] = d.cartas[d.players[dni]["initialcard"]]["priority"]

    
    for carta in range(len(list_value)-1):

'''

#Restaura los puntos de los jugadores en la partida a 20.

def resetPoints():

    for dni in d.game:

        d.players[dni]["points"] = 20

#Verifica que minimo hayan dos jugadores en la partida.

def checkMinimun2PlayerWithPoints():

    len_jugadores = len(d.game)

    try:
        if len_jugadores < 2:
            
            raise ValueError("The number of player must to be bigger than two. \n")
    
    except ValueError as e:

        print(e)

#Ordena a los jugadores en base a su puntación.
def orderPlayersByPoints(listaJugadores):

    for pasadas in range(len(listaJugadores)-1):

        for i in range(len(listaJugadores)-1-pasadas):

            if d.players[listaJugadores[i]]["points"] > d.players[listaJugadores[i+1]]["points"]:
                listaJugadores[i],listaJugadores[i+1] = listaJugadores[i+1],listaJugadores[i] 

    return listaJugadores

#Ordena los jugadores de la partida segun su prioridad
def orderAllPlayers():
    #Extraemos los jugadores de la partida.
    list_players = []
    for player in d.game:
        list_players.append(player)

    
    #Ordenamos a los jugadores en base a su prioridad.
    for pasadas in range(len(list_players)-1):

        for i in range(len(list_players)-1-pasadas):

            if d.players[list_players[i]]["priority"] > d.players[list_players[i+1]]["priority"]:
                list_players[i],list_players[i+1] = list_players[i+1],list_players[i] 

    #Buscamos al jugador que tiene bank == True y le ponemos primero.
    for player in list_players:

        if d.players[player]["bank"] == True:
            #Encontramos su posicion en la lista despues de haberlos ordenado segun prioridad 
            #y le sumamos 1 posicion a su posicion porque cuando le insertemos al principio al haber un elemento esta suera una posicion mayor.
            position = list_players.index(player) +1
            #Insertamos al jugador en primera posicion.
            list_players.insert(0,player)
            #Le eliminamos de la posicion que ocupaba anteriormente.
            del(list_players[position])
        
   
    #Devolvemos la lista ordenada segun prioridad y con la banca al principio.
    return list_players