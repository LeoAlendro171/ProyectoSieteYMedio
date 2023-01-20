DROP DATABASE IF EXISTS Siete_Y_Medio;
CREATE DATABASE Siete_Y_Medio CHARACTER SET utf8mb4;
USE Siete_Y_Medio;

create table Player(
	DNI varchar(255) primary key,
    Nombre varchar(100)not null,
    Type_perfil varchar(255),
    Human tinyint (1),
    priority varchar(100),
    Is_bank tinyint(1),
    Bet_points varchar(255),
    Round_points varchar(100)
);

create table Deck (
	Deck_id char(3) primary key,
    Deck_name varchar(255)
);

create table Card(
	ID_Card varchar(255) primary key,
    Card_name varchar(100) not null,
    Card_value varchar(255),
    Card_priority tinyint not null,
    Card_real_value varchar(255) not null,
    deck_id char(3) ,
    FOREIGN KEY (Deck_id) references Deck (Deck_id)
);

/*Palo_Carta
create Table Stick (
	ID_Palo Varchar(255) not null,
    Nombre varchar(255) not null ,
    ID_Card varchar(255) not null ,
    foreign key (ID_Card) references Card(ID_Card)
);*/


create table Cardgame (
	Cardgame_id int primary key,
    Players varchar(255),
    Rounds varchar(255),
    Deck_id char(3),
    start_hour timestamp,
    end_hour timestamp,
    foreign key (Deck_id) references Deck (Deck_id)
);

create table Player_game(
	Cardgame_id int  primary key,
    DNI varchar(255) not null ,
	Initial_card_id varchar(255) not null ,
    Starting_points tinyint,
    Ending_point tinyint,
     foreign key (Cardgame_id) references Cardgame(Cardgame_id),
    foreign key (DNI) references Player(DNI),
    foreign key (Initial_card_id) references Card (ID_Card)
    
);
/*Ronda*/
create table Player_game_round (
	Cardgame_id int,  #Baraja español por defecto
    Round_num int auto_increment primary key, #Cont(ronda)
    DNI varchar(255),
    Starting_round_points varchar(255),
    Ending_round_points varchar(255),
    foreign key (cardgame_id) references Player_game (cardgame_id),
    foreign key  (DNI) references Player_game (DNI)
);
create view Ranking as select 
(sum(Pg.Ending_point) - sum(Pg.Starting_points)) as 'Ganancias Obtenidas' , sum(Pg.Cardgame_id) as 'partidasJugadas', (sum(Cg.start_hour) - sum(Cg.end_hour)) 'MinutosJugados' from Player_game Pg
inner join Cardgame Cg on Cg.Cardgame_id = Pg.Cardgame_id;

alter table Cardgame modify start_hour timestamp NULL DEFAULT CURRENT_TIMESTAMP;
alter table Cardgame modify end_hour timestamp  NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;