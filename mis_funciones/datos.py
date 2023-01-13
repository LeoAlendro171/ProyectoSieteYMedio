cartas = {
    "O01": {"literal": "As de Oros", "value": 1, "priority": 4, "realValue": 1},
    "O02": {"literal": "Dos de Oros", "value": 2, "priority": 4, "realValue": 2},
    "O03": {"literal": "Tres de Oros", "value": 3, "priority": 4, "realValue": 3},
    "O04": {"literal": "Cuatro de Oros", "value": 4, "priority": 4, "realValue": 4},
    "O05": {"literal": "Cinco de Oros", "value": 5, "priority": 4, "realValue": 5},
    "O06": {"literal": "Seis de Oros", "value": 6, "priority": 4, "realValue": 6},
    "O07": {"literal": "Siete de Oros", "value": 7, "priority": 4, "realValue": 7},
    "O08": {"literal": "Ocho de Oros", "value": 8, "priority": 4, "realValue": 0.5},
    "O09": {"literal": "Nueve de Oros", "value": 9, "priority": 4, "realValue": 0.5},
    "O10": {"literal": "Diez de Oros", "value": 10, "priority": 4, "realValue": 0.5},
    "O11": {"literal": "Once de Oros", "value": 11, "priority": 4, "realValue": 0.5},
    "O12": {"literal": "Doce de Oros", "value": 12, "priority": 4, "realValue": 0.5},

    "C01": {"literal": "As de Copas", "value": 1, "priority": 3, "realValue": 1},
    "C02": {"literal": "Dos de Copas", "value": 2, "priority": 3, "realValue": 2},
    "C03": {"literal": "Tres de Copas", "value": 3, "priority": 3, "realValue": 3},
    "C04": {"literal": "Cuatro de Copas", "value": 4, "priority": 3, "realValue": 4},
    "C05": {"literal": "Cinco de Copas", "value": 5, "priority": 3, "realValue": 5},
    "C06": {"literal": "Seis de Copas", "value": 6, "priority": 3, "realValue": 6},
    "C07": {"literal": "Siete de Copas", "value": 7, "priority": 3, "realValue": 7},
    "C08": {"literal": "Ocho de Copas", "value": 8, "priority": 3, "realValue": 0.5},
    "C09": {"literal": "Nueve de Copas", "value": 9, "priority": 3, "realValue": 0.5},
    "C10": {"literal": "Diez de Copas", "value": 10, "priority": 3, "realValue": 0.5},
    "C11": {"literal": "Once de Copas", "value": 11, "priority": 3, "realValue": 0.5},
    "C12": {"literal": "Doce de Copas", "value": 12, "priority": 3, "realValue": 0.5},

    "E01": {"literal": "As de Espadas", "value": 1, "priority": 2, "realValue": 1},
    "E02": {"literal": "Dos de Espadas", "value": 2, "priority": 2, "realValue": 2},
    "E03": {"literal": "Tres de Espadas", "value": 3, "priority": 2, "realValue": 3},
    "E04": {"literal": "Cuatro de Espadas", "value": 4, "priority": 2, "realValue": 4},
    "E05": {"literal": "Cinco de Espadas", "value": 5, "priority": 2, "realValue": 5},
    "E06": {"literal": "Seis de Espadas", "value": 6, "priority": 2, "realValue": 6},
    "E07": {"literal": "Siete de Espadas", "value": 7, "priority": 2, "realValue": 7},
    "E08": {"literal": "Ocho de Espadas", "value": 8, "priority": 2, "realValue": 0.5},
    "E09": {"literal": "Nueve de Espadas", "value": 9, "priority": 2, "realValue": 0.5},
    "E10": {"literal": "Diez de Espadas", "value": 10, "priority": 2, "realValue": 0.5},
    "E11": {"literal": "Once de Espadas", "value": 11, "priority": 2, "realValue": 0.5},
    "E12": {"literal": "Doce de Espadas", "value": 12, "priority": 2, "realValue": 0.5},

    "B01": {"literal": "As de Bastos", "value": 1, "priority": 1, "realValue": 1},
    "B02": {"literal": "Dos de Bastos", "value": 2, "priority": 1, "realValue": 2},
    "B03": {"literal": "Tres de Bastos", "value": 3, "priority": 1, "realValue": 3},
    "B04": {"literal": "Cuatro de Bastos", "value": 4, "priority": 1, "realValue": 4},
    "B05": {"literal": "Cinco de Bastos", "value": 5, "priority": 1, "realValue": 5},
    "B06": {"literal": "Seis de Bastos", "value": 6, "priority": 1, "realValue": 6},
    "B07": {"literal": "Siete de Bastos", "value": 7, "priority": 1, "realValue": 7},
    "B08": {"literal": "Ocho de Bastos", "value": 8, "priority": 1, "realValue": 0.5},
    "B09": {"literal": "Nueve de Bastos", "value": 9, "priority": 1, "realValue": 0.5},
    "B10": {"literal": "Diez de Bastos", "value": 10, "priority": 1, "realValue": 0.5},
    "B11": {"literal": "Once de Bastos", "value": 11, "priority": 1, "realValue": 0.5},
    "B12": {"literal": "Doce de Bastos", "value": 12, "priority": 1, "realValue": 0.5},
}

# Prioridad Poker - Españolas//Diamantes = oros, corazones = copas, picas = espadas, tréboles = bastos

# Diccionario de jugadores
players = {"11115555A":
{"name": "Mario", "human": True, "bank": False, "initialCard": "", "priority": 0, "type": 40, "bet": 4, "points": 0
    ,"cards": [], "roundPoints": 0},
"22225555A":
{"name": "Pedro", "human": True, "bank": False, "initialCard": "", "priority": 0, "type": 40, "bet": 4, "points": 0
    ,"cards": [], "roundPoints": 0},
"99999999A":
{"name": "Alex", "human": False, "bank": False, "initialCard": "", "priority": 0, "type": 40, "bet": 4, "points": 0
 , "cards": [], "roundPoints": 0},
"88888888X":
{"name": "Pepe", "human": True, "bank": False, "initialCard": "", "priority": 0, "type": 50, "bet": 4, "points": 0,
 "cards": [], "roundPoints": 0},
"77777777N":
{"name": "Dario", "human": True, "bank": False, "initialCard": "", "priority": 0, "type": 50, "bet": 4, "points": 0,
 "cards": [], "roundPoints": 0},
"10101010F":
{"name": "Julia", "human": False, "bank": False, "initialCard": "", "priority": 0, "type": 50, "bet": 4, "points": 0,
 "cards": [], "roundPoints": 0},
"11111111E":
{"name": "Silvia", "human": False, "bank": False, "initialCard": "", "priority": 0, "type": 50, "bet": 4, "points": 0,
 "cards": [], "roundPoints": 0},
"22222222D":
{"name": "Carlos", "human": True, "bank": False, "initialCard": "", "priority": 0, "type": 50, "bet": 4, "points": 0,
 "cards": [], "roundPoints": 0}
}

# Provisional///
# Lista <game> donde irán los NIF de todos los jugadores que participan en la partida en cada momento
game = ["99999999A",
        "88888888X",
        "22222222D",
        "11111111E"]

# Lista <mazo> donde irán todos los IDs de las cartas que componen el mazo en cada momento
mazo = []

# Diccionario donde tendremos una serie de variables de contexto a las que podremos acceder desde cualquier sitio
context_game = {"game_players": game}

# Diccionarios para las tablas de BBDD que hay que actualizar durante el juego
cardgame = {"cardgame_id": 0, "players": 0, "start_hour": "hora inicio partida(datetime)", "rounds": 0,
            "end_hour": "hora final de partida (datetime)"}
player_game = {"id_game":{"id_player_1":{"initial_card_id": "card id", "starting_points": 0, "ending_points": 0}}}
player_game_round = {"id_round": {"id_player_1":{"is_bank": " 0 o 1", "bet_points": "apuesta en la ronda",
                                              "starting_round_points": "puntos al inicio de partida",
                                              "cards_value": "puntos obtenidos en la actual ronda",
                                              "ending_round_points": "puntos al final de la ronda"}}}
# ///Provisional

letrasDni = ["T","R","W","A","G","M","Y","F","P","D","X","B","N",
             "J","Z","S","Q","V","H","L","C","K","E"]

titulo_00 = "*"*140+"""
                  _____                              ___              _   _   _         _   __                       
                 /  ___|                            / _ \            | | | | | |       | | / _|                      
                 \ `--.   ___ __   __  ___  _ __   / /_\ \ _ __    __| | | |_| |  __ _ | || |_                       
                   `--. \ / _ \\ \ / / / _ \| '_ \  |  _  || '_ \  / _` | |  _  | / _` || ||  _|                      
                 /\__/ /|  __/ \ V / |  __/| | | | | | | || | | || (_| | | | | || (_| || || |                        
                 \____/  \___|  \_/   \___||_| |_| \_| |_/|_| |_| \__,_| \_| |_/ \__,_||_||_|                        
                                                                                                                 
                                                                                                                 
 _____       _                        _____                               _               _   _____  _  _        
|  ___|     | |                      |_   _|                             | |             (_) |_   _|| || |       
| |__   ___ | |_   ___ __   __  ___    | |    ___  _ __  _ __   __ _   __| |  __ _  ___   _    | |  | || |  __ _ 
|  __| / __|| __| / _ \\ \ / / / _ \    | |   / _ \| '__|| '__| / _` | / _` | / _` |/ __| | |   | |  | || | / _` |
| |___ \__ \| |_ |  __/ \ V / |  __/   | |  |  __/| |   | |   | (_| || (_| || (_| |\__ \ | |  _| |_ | || || (_| |
\____/ |___/ \__| \___|  \_/   \___|   \_/   \___||_|   |_|    \__,_| \__,_| \__,_||___/ |_|  \___/ |_||_| \__,_|"""+\
    "\n"+"*"*140+"\n"

titulo_01 = "*"*140+"""
               ______ ______ ______ ______    ______  _                                
               | ___ \| ___ \|  _  \|  _  \   | ___ \| |                               
               | |_/ /| |_/ /| | | || | | |   | |_/ /| |  __ _  _   _   ___  _ __  ___ 
               | ___ \| ___ \| | | || | | |   |  __/ | | / _` || | | | / _ \| '__|/ __|
               | |_/ /| |_/ /| |/ / | |/ /    | |    | || (_| || |_| ||  __/| |   \__ \
                
               \____/ \____/ |___/  |___/     \_|    |_| \__,_| \__, | \___||_|   |___/
                                                                 __/ |                 
                                                                |___/ """+"\n"+\
    "*"*140+"\n"

titulo_02 = "*"*140+"""
                                              _____        _    _    _                    
                                             /  ___|      | |  | |  (_)                   
                                             \ `--.   ___ | |_ | |_  _  _ __    __ _  ___ 
                                              `--. \ / _ \| __|| __|| || '_ \  / _` |/ __|
                                             /\__/ /|  __/| |_ | |_ | || | | || (_| |\__ \
                                             
                                             \____/  \___| \__| \__||_||_| |_| \__, ||___/
                                                                                __/ |     
                                                                               |___/ """+"\n"+"*"*140+"\n"

titulo_04 = "*"*140+"""
                                            ______                _     _               
                                            | ___ \              | |   (_)              
                                            | |_/ /  __ _  _ __  | | __ _  _ __    __ _ 
                                            |    /  / _` || '_ \ | |/ /| || '_ \  / _` |
                                            | |\ \ | (_| || | | ||   < | || | | || (_| |
                                            \_| \_| \__,_||_| |_||_|\_\|_||_| |_| \__, |
                                                                                   __/ |
                                                                                  |___/ """+"\n"+"*"*140+"\n"

titulo_05 = "*"*140+"""
                                            ______                            _        
                                            | ___ \                          | |       
                                            | |_/ /  ___  _ __    ___   _ __ | |_  ___ 
                                            |    /  / _ \| '_ \  / _ \ | '__|| __|/ __|
                                            | |\ \ |  __/| |_) || (_) || |   | |_ \__ \
                                            
                                            \_| \_| \___|| .__/  \___/ |_|    \__||___/
                                                         | |                           
                                                         |_|"""+"\n"+"*"*140+"\n"

titulo_021 = "*"*140+"""
                       _____        _     _____                          ______  _                                
                      /  ___|      | |   |  __ \                         | ___ \| |                               
                      \ `--.   ___ | |_  | |  \/  __ _  _ __ ___    ___  | |_/ /| |  __ _  _   _   ___  _ __  ___ 
                       `--. \ / _ \| __| | | __  / _` || '_ ` _ \  / _ \ |  __/ | | / _` || | | | / _ \| '__|/ __|
                      /\__/ /|  __/| |_  | |_\ \| (_| || | | | | ||  __/ | |    | || (_| || |_| ||  __/| |   \__ \
                      
                      \____/  \___| \__|  \____/ \__,_||_| |_| |_| \___| \_|    |_| \__,_| \__, | \___||_|   |___/
                                                                                            __/ |                 
                                                                                           |___/"""+"\n"+"*"*140+"\n"
space = " "*45
maxRounds = 5
game_round = 0

Salir = False
flg_00 = True
flg_01 = False
flg_02 = False
flg_021 = False
flg_023 = False
flg_03 = False
flg_04 = False
flg_05 = False