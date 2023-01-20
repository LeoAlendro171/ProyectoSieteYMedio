/*1.Jugador que realiza la apuesta más alta en cada partida,es el que
haya hecho la apuesta más alta en alguna de las rondas de la partida.*/
select pg.Cardgame_id as 'ID_Partida', p.Nombre, max(p.Bet_points)'Maxima_Apuesta' from Player_game pg
inner join  player p on p.DNI = pg.DNI
group by pg.Cardgame_id;

/*2.Cuántos usuarios han sido la banca en cada partida.*/
select count(p.Is_bank) as 'Banca', pg.cardgame_id from player_game pg
inner join player p on p.DNI = pg.DNI
where Is_bank >= 1
group by cardgame_id
;
/*3.Jugador que realiza la apuesta más baja por partida.*/
select pg.Cardgame_id as 'ID_Partida', p.Nombre, min(p.Bet_points)'Maxima_Apuesta' from Player_game pg
inner join  player p on p.DNI = pg.DNI
group by pg.Cardgame_id;

/*4.Calcular la apuesta media de la última ronda de cada partida.*/

select pg.cardgame_id as 'ID_Partida', avg(p.bet_points) as 'Apuesta_Media' from player p
inner join player_game pg on pg.dni = p.dni
group by pg.cardgame_id;

/*5.Cuantas rondas gana la banca en cada partida, PUEDE QUE NO GANE NINGUNA y también se ha de mostrar*/
select cg.cardgame_id as 'ID_Partida', cg.rounds from cardgame cg
inner join player_game pg on pg.cardgame_id = cg.cardgame_id
inner join player p on p.dni = pg.dni
where p.is_bank = 1;


/*6.Porcentaje de rondas ganadas por jugador en cada partida (%), así como su apuesta media de la partida. Un jugador gana
en una ronda cuando es el que obtiene más puntos (mayor diferencia entre los puntos al comenzar y al finalizar la ronda).
PUEDE QUE EN UNA PARTIDA UN JUGADOR,que participe en ella, NO GANE NINGUNA RONDA, también se ha de mostrar.
*/
select pg.cardgame_id , p.dni , cg.rounds ,truncate(((2/sum(pg.cardgame_id))*100),2) as 'porcentaje', avg(p.bet_points) as 'Apuesta_Media',(sum(Pg.Ending_point) - sum(Pg.Starting_points)) as 'diferencia_Punto' from player_game pg
right join player p on p.dni = pg.dni
right join cardgame cg on  cg.cardgame_id = pg.cardgame_id
where human = 1
group by pg.cardgame_id
;
/*7.Lista de partidas ganadas por Bots. El ganador es quien ha conseguido más puntos al finalizar la partida, los puntos
conseguidos son la diferencia entre los puntos que tenía al iniciar la partida y los puntos al acabar.*/
select pg.cardgame_id, (sum(Pg.Ending_point) - sum(Pg.Starting_points)) as 'diferencia_Punto' from player_game pg
inner join player p on p.dni = pg.dni
where human = 0
group by cardgame_id
