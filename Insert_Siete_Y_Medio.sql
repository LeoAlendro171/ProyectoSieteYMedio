use Siete_Y_Medio;

insert into PLayer (DNI,Nombre,Type_perfil,Human,Initial_card_id,priority,Is_bank,Cards_value,Bet_points,Round_points)
values ('21815725H','Mario','40','True','','0','False','','4','0'),
		('67937127A','Pedro','40','True','','0','False','','4','0'),
        ('38296712X','Juan','30','True','','0','False','','4','0'),
        ('44444444H','Boot','50','False','','0','True','','4','0'),
        ('11115555A','Professor','40','False','','0','True','','4','0'),
        ('22225555A','Leo','40','False','','0','True','','4','0')
; 
insert into Deck (Deck_id,Deck_name)
values ('1','ESP-ESP'),('2','PK-PK')
;
insert into Card (ID_Card,Card_name,Card_value,Card_priority,Card_real_value,deck_id)
 values /*1*/('O01','As de Oros','1','4','1','1'), ('O02','Dos de Oros','2','4','2','1'), ('O03','Tres de Oros','3','4','3','1'), ('O04','Cuatro de Oros','4','4','4','1'), ('O05','Cincode Oros','5','4','5','1'), ('O06','Seisde Oros','6','4','6','1'),
 ('O07','Siete de Oros','7','4','7','1'), ('O08','Ocho de Oros','8','4','8','1'), ('O09','Nueve de Oros','9','4','9','1'), ('O10','diez de Oros','10','4','10','1'), ('O11','Oncede Oros','11','4','11','1'), ('O12','Doce de Oros','12','4','12','1'),
        /*2*/('C01','As de Copas','1','3','1','1'), ('C02','Dos de Copas','2','3','2','1'), ('C03','Tres de Copas','3','3','3','1'), ('C04','Cuatro de Copas','4','3','4','1'), ('C05','Cinco de Copas','5','3','5','1'), ('C06','Seis','6','3','6','1'),
('C07','Siete de Copas','7','3','7','1'), ('C08','Ocho de Copas','8','3','8','1'), ('C09','Nueve de Copas','9','3','9','1'), ('C10','Diez de Copas','10','3','10','1'), ('C11','Once de Copas','11','3','11','1'), ('C12','Doce de Copas','12','3','12','1'),
        /*3*/('E01','Uno de Espada','1','2','1','1'), ('E02','Dos de Espada','2','2','2','1'), ('E03','Tres de Espada','3','2','3','1'), ('E04','Cuatro','4','2','4','1'), ('E05','Cinco','5','2','5','1'), ('E06','Seis de Espada','6','2','6','1'),
('E07','Siete de Espada','7','2','7','1'), ('E08','Ocho de Espada','8','2','8','1'), ('E09','Nueve de Espada','9','2','9','1'), ('E10','Diez de Espada','10','2','10','1'), ('E11','Once de Espada','11','2','11','1'), ('E12','Doce de Espada','12','2','12','1'),
		/*4*/('B01','As de Basto','1','1','2','1'), ('B02','Dos de Basto','2','1','2','1'), ('B03','Tres de Basto','3','1','3','1'), ('B04','Cuatro de Basto','4','1','4','1'), ('B05','Cinco de Basto','5','1','5','1'), ('B06','Seis de Basto','6','1','6','1'),
('B07','Siete de Basto','7','1','7','1'), ('B08','Ocho de Basto','8','1','8','1'), ('B09','Nueve de Basto','9','1','9','1'), ('B10','Diez de Basto','10','1','10','1'), ('B11','Once de Basto','11','1','11','1'), ('B12','Doce de Basto','12','1','12','1'),

		/*1*/('D01','Uno  de Diamante','1','4','1','2'),('D02','Dos de Diamante','2','4','2','2'),('D03','Tres de Diamante','3','4','3','2'),('D04','Cuatro de Diamante','4','4','4','2'),('D05','Cinco de Diamante','5','4','5','2'),('D06','Seis de Diamante','6','4','6','2'),
('D07','Siete de Diamante','7','4','7','2'),('D08','Ocho de Diamante','8','4','8','2'),('D09','Nueve de Diamante','9','4','9','2'),('D10','Diez de Diamante','10','4','10','2'),('D11','Once de Diamante','11','4','11','2'),('D12','Doce de Diamante','12','4','12','2'),
		/*2*/('C01','As de Corazon','1','3','1','2'),('C02','Dos de Corazon','2','3','2','2'),('C03','Tres de Corazon','3','3','3','2'),('C04','Cuatro de Corazon','4','3','4','2'),('C05','Cinco de Corazon','5','3','5','2'),('C06','Seis de Corazon','6','3','6','2'),
('C07','Siete de Corazon','7','3','7','2'),('C08','Ocho de Corazon','8','3','8','2'),('C09','Nueve de Corazon','9','3','9','2'),('C10','Diez de Corazon','10','3','10','2'),('C11','Oncede Corazon','11','3','11','2'),('C12','Doce de Corazon','12','3','12','2'),
		/*3*/('P01','de Pica','','2','','2'),('P02','Dos de Pica','2','2','2','2'),('P03','Tres de Pica','3','2','3','2'),('P04','Cuatro de Pica','4','2','4','2'),('P05','Cinco de Pica','5','2','5','2'),('P06','de Pica','6','2','6','2'),
('P07','Siete de Pica','7','2','7','2'),('P08','Ocho de Pica','8','2','8','2'),('P09','Nueve de Pica','9','2','9','2'),('P10','Diez de Pica','10','2','10','2'),('P11','Once de Pica','11','2','11','2'),('P12','de Pica','12','2','12','2'),
		/*4*/('T01','de Trebol','1','1','1','2'),('T02','Dos de Trebol','2','1','2','2'),('T03','Tres de Trebol','3','1','3','2'),('T04','Cuatro de Trebol','4','1','4','2'),('T05','Cinco de Trebol','5','1','5','2'),('T06','Sies de Trebol','6','1','6','2'),
('T07','Siete de Trebol','7','1','7','2'),('T08','Ocho de Trebol','8','1','8','2'),('T09','Nueve de Trebol','9','1','9','2'),('T10','Diez de Trebol','10','1','10','2'),('T11','Once de Trebol','11','1','11','2'),('T12','Doce de Trebol','12','1','12','2')
;
