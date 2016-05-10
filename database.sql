CREATE TABLE ride (
    driver_id INTEGER NULL,
    passenger_id INTEGER NULL,
    passenger_location VARCHAR(100) NOT NULL,
    passenger_destination VARCHAR(100) NOT NULL,
    pick_up_time VARCHAR(50) NULL
);

CREATE TABLE passenger (
    passenger_id SERIAL PRIMARY KEY,
    firstname VARCHAR(30) NULL,
    lastname VARCHAR(30) NOT NULL
);

CREATE TABLE driver (
    driver_id SERIAL PRIMARY KEY,
    firstname VARCHAR(30) NULL,
    lastname VARCHAR(30) NOT NULL,
    driver_location VARCHAR(100) NULL
);

INSERT INTO passenger (firstname, lastname)
VALUES ('Harry', 'Potter'),
(NULL, 'Weasley'),
('Draco', 'Malfoy'),
('Hermoine', 'Granger');

INSERT INTO driver (firstname, lastname, driver_location)
VALUES (NULL, 'Snape', 'Forbidden Forest'),
('Professor', 'Dumbledore' , 'Kings Cross Station, Platform 9.75'),
(NULL, 'Hagrid', 'Gringotts'),
('Neville', 'Longbottom', 'Grimmauld Place');

INSERT INTO ride (passenger_location, passenger_destination, pick_up_time)
VALUES ('Forbidden Forest', 'Ministry of Magic', 2016-06-12 13:00:00),
('Hogwarts', 'Malfoy Mansion', 2016-06-20 16:00:00),
('Malfoy Mansion', 'Hogwarts', 2016-06-20 16:15:00),
('Grimmauld Place', 'Diagon Alley', 2016-07-4 11:30:00);
