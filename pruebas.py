import funciones as f
import datos as d
import datos_pruebas as dp

for card in d.cartas_poker:
    d.mazo.append(card)
print(d.mazo)
f.orderAllPlayers()