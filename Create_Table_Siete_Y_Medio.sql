DROP DATABASE IF EXISTS Siete_Y_Medio;
CREATE DATABASE Siete_Y_Medio CHARACTER SET utf8mb4;
USE Siete_Y_Medio;

create table PLayer(
	DNI varchar(255) primary key,
    Nombre varchar(100)not null,
    Type_perfil varchar(255),
    Human tinyint (1),
    Initial_card_id char(5),
    priority varchar(100),
    Is_bank tinyint(1),
    Cards_value decimal (4,1),
    Bet_points tinyint,
    Round_points varchar(100)
);

create table Deck (
	Deck_id char(3) primary key,
    Deck_name varchar(255)
);

create table Card(
	ID_Card int primary key,
    Card_name varchar(100) not null,
    Card_value Decimal(3,1)not null ,
    Card_priority tinyint not null,
    Card_real_value tinyint not null,
    deck_id char(3) NOT NULL,
    FOREIGN KEY (Deck_id) references Deck (Deck_id) 
);

create table Cardgame (
	Cardgame_id int primary key,
    Player tinyint,
    Rounds tinyint,
    start_hours datetime,
    end_hour datetime,
    Deck_id char(3),
    foreign key (Deck_id) references Deck (Deck_id)
);

create table Palyer_game(
	Cardgame_id int,
    Player_id varchar(255),
    Starting_points tinyint,
    Ending_point tinyint,
    foreign key (Cardgame_id) references Cardgame(Cardgame_id),
    foreign key (Player_id) references Player(DNI)
);


create table Player_game_round (
	Cardgame_id int, 
    Round_num tinyint primary key,
    Player_id varchar(255),
    Starting_round_points tinyint,
    Ending_round_points tinyint,
    foreign key (cardgame_id) references Cardgame (cardgame_id),
    foreign key  (player_id) references Player (DNI)
);

create table Ranking (
	Ganancias_obtenida int,
    Partida_Jugadas varchar(255),
    Minutos_Jugados varchar (255)

);