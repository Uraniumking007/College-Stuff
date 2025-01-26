create database cieDB;
use cieDB;

CREATE TABLE
    Users1 (
        user_id INT PRIMARY KEY,
        name char(50) NOT NULL,
        email char(100) UNIQUE NOT NULL,
        password char(255) NOT NULL,
        contact_number char(15),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

INSERT INTO Users1 (user_id, name, email, password, contact_number) VALUES 
(1, 'Aarav Sharma', 'aarav.sharma@gmail.com', 'password123', '9876543210') ,
(2, 'Aditi Patel', 'aditi.patel@gmail.com', 'password123', '9876543211') ,
(3, 'Rohit Verma', 'rohit.verma@gmail.com', 'password123', '9876543212') ,
(4, 'Nisha Iyer', 'nisha.iyer@gmail.com', 'password123', '9876543213') ,
(5, 'Rajesh Kapoor', 'rajesh.kapoor@gmail.com', 'password123', '9876543214'), 
(6, 'Meera Nair', 'meera.nair@gmail.com', 'password123', '9876543215') ,
(7, 'Akash Gupta', 'akash.gupta@gmail.com', 'password123', '9876543216'), 
(8, 'Sneha Desai', 'sneha.desai@gmail.com', 'password123', '9876543217') ,
(9, 'Karan Malhotra', 'karan.malhotra@gmail.com', 'password123', '9876543218'),
(10, 'Anjali Reddy', 'anjali.reddy@gmail.com', 'password123', '9876543219') ,
(11, 'Vikram Singh', 'vikram.singh@gmail.com', 'password123', '9876543220');

CREATE TABLE
    User_Payment_Info (
        payment_id INT PRIMARY KEY,
        user_id INT,
        card_number char(16),
        card_type char(20),
        expiry_date DATE,
        billing_address cchar(255),
        FOREIGN KEY (user_id) REFERENCES Users (user_id)
    );

INSERT into
    User_Payment_Info
VALUES
    (
        1,
        1,
        '1234567812345678',
        'Visa',
        TO_DATE ('2025-12-31', 'YYYY-MM-DD'),
        '123, MG Road, Mumbai'
    ) (
        2,
        2,
        '2345678923456789',
        'MasterCard',
        TO_DATE ('2026-05-30', 'YYYY-MM-DD'),
        '456, Brigade Road, Bangalore'
    ) (
        3,
        3,
        '3456789034567890',
        'Visa',
        TO_DATE ('2027-08-15', 'YYYY-MM-DD'),
        '789, Anna Salai, Chennai'
    ) (
        4,
        4,
        '4567890145678901',
        'Rupay',
        TO_DATE ('2024-11-11', 'YYYY-MM-DD'),
        '101, Park Street, Kolkata'
    ) (
        5,
        5,
        '5678901256789012',
        'American Express',
        TO_DATE ('2028-02-20', 'YYYY-MM-DD'),
        '202, Connaught Place, Delhi'
    ) (
        6,
        6,
        '6789012367890123',
        'Visa',
        TO_DATE ('2025-07-19', 'YYYY-MM-DD'),
        '505, Banjara Hills, Hyderabad'
    ) (
        7,
        7,
        '7890123478901234',
        'MasterCard',
        TO_DATE ('2026-03-14', 'YYYY-MM-DD'),
        '707, Nungambakkam, Chennai'
    ) (
        8,
        8,
        '8901234589012345',
        'Rupay',
        TO_DATE ('2027-09-25', 'YYYY-MM-DD'),
        '909, MG Road, Pune'
    ) (
        9,
        9,
        '9012345690123456',
        'Visa',
        TO_DATE ('2025-12-10', 'YYYY-MM-DD'),
        '606, MG Road, Indore'
    ) (
        10,10,'1234567801234567','MasterCard',TO_DATE ('2028-05-22', 'YYYY-MM-DD'),'302, Camac Street, Kolkata')