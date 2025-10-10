-- C.K PITHAWALA COLLEGE OF ENGINEERING &TECHNOLGY B.E-II YEAR SEMESTER III 
-- Database Management Systems(3130703) 
-- INFORMATIONAL TECHNOLOGY ENGINEERING DEPARTMENT
-- Practical Exam Batch A1 

use cieDB;

CREATE TABLE
    Users (
        user_id INT PRIMARY KEY,
        name char(50) NOT NULL,
        email char(100) UNIQUE NOT NULL,
        password char(255) NOT NULL,
        contact_number char(15),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

INSERT INTO
    Users (user_id, name, email, password, contact_number)
VALUES
    (
        1,
        'Aarav Sharma',
        'aarav.sharma@gmail.com',
        'password123',
        '9876543210'
    ),
    (
        2,
        'Aditi Patel',
        'aditi.patel@gmail.com',
        'password123',
        '9876543211'
    ),
    (
        3,
        'Rohit Verma',
        'rohit.verma@gmail.com',
        'password123',
        '9876543212'
    ),
    (
        4,
        'Nisha Iyer',
        'nisha.iyer@gmail.com',
        'password123',
        '9876543213'
    ),
    (
        5,
        'Rajesh Kapoor',
        'rajesh.kapoor@gmail.com',
        'password123',
        '9876543214'
    ),
    (
        6,
        'Meera Nair',
        'meera.nair@gmail.com',
        'password123',
        '9876543215'
    ),
    (
        7,
        'Akash Gupta',
        'akash.gupta@gmail.com',
        'password123',
        '9876543216'
    ),
    (
        8,
        'Sneha Desai',
        'sneha.desai@gmail.com',
        'password123',
        '9876543217'
    ),
    (
        9,
        'Karan Malhotra',
        'karan.malhotra@gmail.com',
        'password123',
        '9876543218'
    ),
    (
        10,
        'Anjali Reddy',
        'anjali.reddy@gmail.com',
        'password123',
        '9876543219'
    ),
    (
        11,
        'Vikram Singh',
        'vikram.singh@gmail.com',
        'password123',
        '9876543220'
    );

CREATE TABLE
    User_Payment_Info (
        payment_id INT PRIMARY KEY,
        user_id INT,
        card_number char(16),
        card_type char(20),
        expiry_date DATE,
        billing_address char(255),
        FOREIGN KEY (user_id) REFERENCES Users (user_id)
    );

INSERT into
    User_Payment_Info (
        payment_id,
        user_id,
        card_number,
        card_type,
        expiry_date,
        billing_address
    )
VALUES
    -- (
    --         1,
    --         1,
    --         '1234567812345678',
    --         'Visa',
    --         '2025-12-31',
    --         '123, MG Road, Mumbai'
    --     ),
    (
        3,
        3,
        '3456789034567890',
        'Visa',
        '2027-08-15',
        '789, Anna Salai, Chennai'
    ),
    (
        6,
        6,
        '6789012367890123',
        'Visa',
        '2025-07-19',
        '505, Banjara Hills, Hyderabad'
    ),
    (
        9,
        9,
        '9012345690123456',
        'Visa',
        '2025-12-10',
        '606, MG Road, Indore'
    );
CREATE TABLE
    Movies (
        movie_id INT PRIMARY KEY,
        title char(100) NOT NULL,
        genre char(50),
        duration INT,
        rating decimal(3, 1),
        release_date DATE,
        director char(50),
        language char(20)
    );

INSERT INTO
    Movies (
        movie_id,
        title,
        genre,
        duration,
        rating,
        release_date,
        director,
        language
    )
VALUES
    (
        1,
        'Baahubali',
        'Action',
        165,
        8.5,
        '2015-07-10',
        'S.S. Rajamouli',
        'Telugu'
    ),
    (
        2,
        '3 Idiots',
        'Comedy',
        145,
        8.4,
        '2009-12-25',
        'Rajkumar Hirani',
        'Hindi'
    ),
    (
        3,
        'Kabir Singh',
        'Drama',
        172,
        7.0,
        '2019-06-21',
        'Sandeep Vanga',
        'Hindi'
    ),
    (
        4,
        'Dangal',
        'Biography',
        160,
        8.7,
        '2016-12-23',
        'Nitesh Tiwari',
        'Hindi'
    ),
    (
        5,
        'K.G.F: Chapter 1',
        'Action',
        156,
        8.2,
        '2018-12-21',
        'Prashanth Neel',
        'Kannada'
    ),
    (
        6,
        'Chennai Express',
        'Romance',
        141,
        6.9,
        '2013-08-09',
        'Rohit Shetty',
        'Hindi'
    ),
    (
        7,
        'Drishyam',
        'Thriller',
        163,
        8.1,
        '2015-07-31',
        'Nishikant Kamat',
        'Hindi'
    ),
    (
        8,
        'Padmaavat',
        'Historical',
        164,
        7.0,
        '2018-01-25',
        'Sanjay Leela Bhansali',
        'Hindi'
    ),
    (
        9,
        'Bajrangi Bhaijaan',
        'Drama',
        163,
        8.0,
        '2015-07-17',
        'Kabir Khan',
        'Hindi'
    ),
    (
        10,
        'Dil Chahta Hai',
        'Comedy',
        183,
        8.1,
        '2001-08-10',
        'Farhan Akhtar',
        'Hindi'
    );

CREATE TABLE
    Shows (
        show_id INT PRIMARY KEY,
        movie_id INT,
        theater_id INT,
        start_time TIMESTAMP,
        end_time TIMESTAMP,
        screen_number INT,
        FOREIGN KEY (movie_id) REFERENCES Movies (movie_id)
    );

INSERT INTO
    Shows (
        show_id,
        movie_id,
        theater_id,
        start_time,
        end_time,
        screen_number
    )
VALUES
    (
        1,
        1,
        1,
        '2024-10-11 18:30:00',
        '2024-10-11 21:15:00',
        1
    ),
    (
        2,
        2,
        2,
        '2024-10-11 20:00:00',
        '2024-10-11 22:30:00',
        2
    ),
    (
        3,
        3,
        3,
        '2024-10-11 19:00:00',
        '2024-10-11 21:45:00',
        3
    ),
    (
        4,
        4,
        4,
        '2024-10-11 17:30:00',
        '2024-10-11 20:10:00',
        4
    ),
    (
        5,
        5,
        5,
        '2024-10-11 18:00:00',
        '2024-10-11 20:50:00',
        5
    ),
    (
        6,
        6,
        1,
        '2024-10-12 14:30:00',
        '2024-10-12 16:45:00',
        1
    ),
    (
        7,
        7,
        2,
        '2024-10-12 15:00:00',
        '2024-10-12 17:20:00',
        2
    ),
    (
        8,
        8,
        3,
        '2024-10-12 19:30:00',
        '2024-10-12 22:00:00',
        3
    ),
    (
        9,
        9,
        4,
        '2024-10-12 21:00:00',
        '2024-10-12 23:45:00',
        4
    ),
    (
        10,
        10,
        5,
        '2024-10-12 18:45:00',
        '2024-10-12 21:15:00',
        5
    );

-- Perform the following SQL queries[ODD]: 

-- 1. Display title of Movie. 
select title from Movies;

-- 2. Update the contact number from the user table whose name is ‘Rajesh Kapoor’. 
select * from users where name = 'Rajesh Kapoor';

update users set contact_number = '9876543256' where name = 'Rajesh Kapoor';

-- 3. Display the record from the user table whose name starts with ‘R’. 
select * from users where name like 'R%';

-- 4. Display the start time and movie name whose movie id is 5. 
-- Movie, shows
select
    m.title,
    s.start_time
from
    Movies m
    join Shows s on s.show_id = m.movie_id
where
    m.movie_id = 5;

-- 5. Delete the record from User_Payment_Info whose card type is ’Visa’. 
set foreign_key_checks = 1;
select * from user_payment_info;
delete from user_payment_info where card_type = 'Visa';

-- Perform the following SQL queries[Even]: 
-- 1. Display user name and email of users.. 
-- 2. Update the title ‘Mission3’ from whose director ‘Nitesh Tiwari’. 
-- 3. Display the record from the User table whose name ends with ‘a’.
-- 4. Display the end time and movie name whose movie id is 2. 
-- 5. Delete the record from User_Payment_Info whose card type is ’Rupay’.