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
    status CHAR(24) DEFAULT 'Active',  Active, Completed, Cancelled
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







 Filter va Aggrogate functions


 where  /  between  / like / order by / limit / group by / gt / lt / count / sum / max / min 



where -> eng assoiy  filter qiluvchi functions 

select * from Track 
WHERE AlbumId = 2 or/and GenreId  = 2


 between > where bn ishlatiladi va oraliqdan malumot ob berad

 select * from Track 
WHERE Milliseconds  BETWEEN 50000 and 3000000
WHERE Name BETWEEN "a" and "b"
WHERE birth_date BETWEEN '1955-15-02' and '2026-01-01'



 like > yozuvlar ichidan topish imkonini beradi

 select * from Track 
WHERE Name like 'Fast as a Shark'
WHERE Name like 'F%'  F blan boshlanadigan Name lar
WHERE Name like '%A'  va blan tugidigan Name lar
WHERE Name like '%or%'  agar name ichida or bsa topib berad 
WHERE lower(Name) like lower('%A') 


 order > Sartirovkasini belgilaydi  asc(1..100) desc(100..1)
 ASC() / DESC() - Ascii jadval bn kelad harf la bn

select * from Track 
ORDER BY TrackId  DESC
 


limit > malumotlar olishda limit qoyb beradi va pagintion xosil bolas
 offset > malum bir miqdorda malumotlarni tashab ketadi
 Offset har doim limit bn ishlatiladi

select * from Track 
where (Milliseconds Between 50000 and 100000) or name LIKE '%fast%'
order by TrackId 
limit 5

select * from Track 
where (Milliseconds Between 50000 and 100000) or name LIKE '%fast%'
order by TrackId 
limit 5 OFFSET 5



gt (greather than) 
lt (lower than)


select * from Track
where Milliseconds  > 100000
where Milliseconds  < 100000




sum > barcha ustunlarni yigindisinni oladi
 
select 	sum(TrackId )FROM  Track   obsh 6 137 256
select 	sum(Milliseconds ) FROM Track   obsh  1 378 778 040
select 	sum(UnitPrice) FROM Track   obsh  3 680,969999997



 group by > elementlarni ustuniga qarab guruhlarga ajratadi

select sum(UnitPrice) as "Total Price",*from Track 
GROUP BY GenreId   1 id dagi Genre  1 284 + foyda i td



Count 


select sum(UnitPrice) as "Total Price", COUNT(TrackId) as "Count", *from Track 
 1 id dagi albumda 10 ta Track Id bor kan obsh  total price 99$
GROUP BY GenreId   1 id dagi Genre  1 284 + foyda i td


 Max, min > Eng kotta va kichkina qiymatlarni olib beradi

SELECT Max(Milliseconds), * from Track  
SELECT Min(Milliseconds), * from Track  


