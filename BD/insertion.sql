INSERT INTO CATEGORIE VALUES  
(1, 'Guide orange', 'ff8000'), (2, 'INRS','ffff00'),
(3, 'INERIS FDRE','00ff00'),(4, 'CEDRE','ff0000'),(5, 'Air Liquide','0000ff'),(8, 'Valeurs toxico','ff00ff'),
(9, 'BIG','00ffff'),(10, 'Encyclos gaz','8000ff'),(11, 'VSTAF','0080C0'),(12, 'Classeur opérationnel RENZO','80ff80'),
(13, 'Mmento formules RCH pour FOAD','80ff00'),(14, 'BAO RCH 2021','ff8000'),(15, 'ALHOA','ff0080');

INSERT INTO GRADE VALUES  
(1, 'Caporal'),(2, 'Sergent'),(3, 'Sergent-Chef'),(4, 'Adjudant'),(5, 'Adjudant-Chef');

INSERT INTO CASERNE VALUES 
(1, 'Caserne 1', '1 rue de la caserne');

INSERT INTO UTILISATEUR VALUES  
(1, 'LUDMANN', 'Dorianne', 'dorianne','XxDarkSasukexX',1,-1,1)

INSERT INTO TAG VALUES --(idTag, nomTag, niveauProtection, couleurTag)
(1, "Feu", 0, "ff9700"),
(2, "Montagne", 0, "4ae9c7"),
(3, "Maritime", 0, "128be9"),
(4, "Tempêtes", 0, "cacaca"),
(5, "Forêt", 0, "00750c"),
(6, "Faune", 0, "f8fa84"),
(7, "Flore", 0, "3eab49"),
(8, "Chimique", 0, "823a9f"),
(9, "Uranium", 0, "30ec35"),
(10, "Evacuation", 0, "e381f7"),
(11, "Feu de sillo", 0, "ff9700"),
(12, "Feu de forêt", 0, "ff9700"),
(13, "Arbre tombé", 0, "259a31"),
(14, "Fuite d'eau", 0, "95e3d0"),
(15, "Nucléaire", 5, "30ec35"),
(16, "Confinement", 0, "4e4c68"),
(17, "Personne piégée", 0, "4e4c68"),
(18, "Eboulement", 0, "582d31"),
(19, "Effondrement", 0, "826265"),
(20, "Pont", 0, "9995e3"),
(21, "Suicide", 0, "110e41"),
(22, "Hauteur", 0, "1fa4a0"),
(23, "AVC", 0, "f65564"),
(24, "Malaise", 0, "621119"),
(25, "Forte chaleur", 0, "f76b0a");