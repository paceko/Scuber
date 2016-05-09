CREATE TABLE models (
    id SERIAL PRIMARY KEY,
    year INTEGER NOT NULL,
    brand_name VARCHAR(50) NULL,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE brands (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    founded INTEGER,
    headquarters VARCHAR(50),
    discontinued INTEGER
);

INSERT INTO brands (name, founded, headquarters, discontinued)
VALUES ('Ford', 1903, 'Dearborn, MI', NULL),
('Chrysler', 1925, 'Auburn Hills, Michigan', NULL),
('Citroen', 1919, 'Saint-Ouen, France', NULL),
('Hillman', 1907, 'Ryton-on-Dunsmore, England', 1981),
('Chevrolet', 1911, 'Detroit, Michigan', NULL),
('Cadillac', 1902, 'New York City, NY', NULL);