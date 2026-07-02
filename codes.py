CREATE TABLE car_categories (
    id INT,
    name CHAR(24),
    price_per_day INT,
    PRIMARY KEY (id)
);

CREATE TABLE cars (
    id INT,
    brand CHAR(24),
    model CHAR(24),
    year INT,
    license_plate CHAR(15),
    is_available BOOLEAN DEFAULT TRUE,
    category_id INT,
    PRIMARY KEY (id),
    FOREIGN KEY (category_id) REFERENCES car_categories(id)
);

CREATE TABLE clients (
    id INT,
    first_name CHAR(24),
    last_name CHAR(24),
    phone CHAR(20),
    email CHAR(34),
    passport_seria CHAR(10),
    PRIMARY KEY (id)
);

CREATE TABLE rentals (
    id INT,
    rental_date DATE,
    return_date DATE,
    total_amount INT,
    status CHAR(24) DEFAULT 'Active', -- Active, Completed, Cancelled
    car_id INT,
    client_id INT,
    PRIMARY KEY (id),
    FOREIGN KEY (car_id) REFERENCES cars(id),
    FOREIGN KEY (client_id) REFERENCES clients(id)
);




CRUD


CREATE

INSERT INTO car_categories (id, name, price_per_day) VALUES 
(1, 'Sedan', 300000),
(2, 'SUV', 500000),
(3, 'Hypercar', 1500000);

INSERT INTO cars (id, brand, model, year, license_plate, category_id) VALUES 
(10, 'Chevrolet', 'Malibu 2', 2024, '01A777AA', 1),
(11, 'BYD', 'Song Plus', 2025, '01B888BB', 2),
(12, 'Ford', 'Mustang GT', 2023, '01M001GG', 3);

INSERT INTO clients (id, first_name, last_name, phone, email, passport_seria) VALUES 
(1, 'Anvar', 'Sultonov', '+998901112233', 'anvar@gmail.com', 'AA1234567'),
(2, 'Dilshod', 'Raxmatov', '+998934445566', 'dilshod@gmail.com', 'AB9876543');



READ

SELECT * FROM cars WHERE is_available = TRUE;

SELECT brand, model, license_plate FROM cars WHERE id = 12;

SELECT email, phone FROM clients WHERE id = 1;



UPDATE

UPDATE cars 
SET is_available = FALSE 
WHERE id = 12;

UPDATE clients 
SET phone = '+998997777777' 
WHERE id = 2;



DELETE

DELETE FROM cars 
WHERE id = 10;

DELETE FROM clients 
WHERE id = 1;