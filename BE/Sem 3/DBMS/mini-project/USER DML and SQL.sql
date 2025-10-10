-- All User Tables

INSERT INTO Users (name, email, password, contact_number) VALUES
('Aarav Sharma', 'aarav.sharma@gmail.com', 'password123', '9876543210'),
('Aditi Patel', 'aditi.patel@gmail.com', 'password123', '9876543211'),
('Rohit Verma', 'rohit.verma@gmail.com', 'password123', '9876543212'),
('Nisha Iyer', 'nisha.iyer@gmail.com', 'password123', '9876543213'),
('Rajesh Kapoor', 'rajesh.kapoor@gmail.com', 'password123', '9876543214'),
('Meera Nair', 'meera.nair@gmail.com', 'password123', '9876543215'),
('Akash Gupta', 'akash.gupta@gmail.com', 'password123', '9876543216'),
('Sneha Desai', 'sneha.desai@gmail.com', 'password123', '9876543217'),
('Karan Malhotra', 'karan.malhotra@gmail.com', 'password123', '9876543218'),
('Anjali Reddy', 'anjali.reddy@gmail.com', 'password123', '9876543219'),
('Vikram Singh', 'vikram.singh@gmail.com', 'password123', '9876543220'),
('Pooja Joshi', 'pooja.joshi@gmail.com', 'password123', '9876543221'),
('Naveen Chauhan', 'naveen.chauhan@gmail.com', 'password123', '9876543222'),
('Riya Sinha', 'riya.sinha@gmail.com', 'password123', '9876543223'),
('Aditya Mehta', 'aditya.mehta@gmail.com', 'password123', '9876543224'),
('Neha Pandey', 'neha.pandey@gmail.com', 'password123', '9876543225'),
('Aman Khanna', 'aman.khanna@gmail.com', 'password123', '9876543226'),
('Kavita Menon', 'kavita.menon@gmail.com', 'password123', '9876543227'),
('Vijay Rao', 'vijay.rao@gmail.com', 'password123', '9876543228'),
('Tina Arora', 'tina.arora@gmail.com', 'password123', '9876543229'),
('Harish Kulkarni', 'harish.kulkarni@gmail.com', 'password123', '9876543230'),
('Swati Saxena', 'swati.saxena@gmail.com', 'password123', '9876543231'),
('Sanjay Bhatt', 'sanjay.bhatt@gmail.com', 'password123', '9876543232'),
('Maya Chatterjee', 'maya.chatterjee@gmail.com', 'password123', '9876543233'),
('Anupam Mukherjee', 'anupam.mukherjee@gmail.com', 'password123', '9876543234');

SELECT * FROM Users;

INSERT INTO User_Preferences (user_id, favorite_genre, preferred_seat_type) VALUES
(1, 'Action', 'Balcony'),
(2, 'Drama', 'VIP'),
(3, 'Comedy', 'Front Row'),
(4, 'Horror', 'Middle Row'),
(5, 'Romance', 'Balcony'),
(6, 'Thriller', 'VIP'),
(7, 'Fantasy', 'Middle Row'),
(8, 'Biography', 'Balcony'),
(9, 'Science Fiction', 'Front Row'),
(10, 'Mystery', 'VIP'),
(11, 'Adventure', 'Middle Row'),
(12, 'Musical', 'Balcony'),
(13, 'Documentary', 'VIP'),
(14, 'Family', 'Middle Row'),
(15, 'Animation', 'Balcony'),
(16, 'Western', 'VIP'),
(17, 'War', 'Front Row'),
(18, 'Crime', 'Middle Row'),
(19, 'Historical', 'Balcony'),
(20, 'Political', 'VIP'),
(21, 'Sports', 'Middle Row'),
(22, 'Psychological', 'Balcony'),
(23, 'Paranormal', 'Front Row'),
(24, 'Espionage', 'VIP'),
(25, 'Disaster', 'Middle Row');

SELECT * FROM User_Preferences;

INSERT INTO User_Roles (role_name) VALUES
('Admin'),
('Customer'),
('Manager'),
('Customer Service'),
('Moderator'),
('Reviewer');



INSERT INTO User_Payment_Info (user_id, card_number, card_type, expiry_date, billing_address) VALUES
(1, '1234567812345678', 'Visa', '2025-12-31', '123, MG Road, Mumbai'),
(2, '2345678923456789', 'MasterCard', '2026-05-30', '456, Brigade Road, Bangalore'),
(3, '3456789034567890', 'Visa', '2027-08-15', '789, Anna Salai, Chennai'),
(4, '4567890145678901', 'Rupay', '2024-11-11', '101, Park Street, Kolkata'),
(5, '5678901256789012', 'American Express', '2028-02-20', '202, Connaught Place, Delhi'),
(6, '6789012367890123', 'Visa', '2025-07-19', '505, Banjara Hills, Hyderabad'),
(7, '7890123478901234', 'MasterCard', '2026-03-14', '707, Nungambakkam, Chennai'),
(8, '8901234589012345', 'Rupay', '2027-09-25', '909, MG Road, Pune'),
(9, '9012345690123456', 'Visa', '2025-12-10', '606, MG Road, Indore'),
(10, '1234567801234567', 'MasterCard', '2028-05-22', '302, Camac Street, Kolkata'),
(11, '2345678912345678', 'Visa', '2026-04-18', '508, Chinnaswamy Stadium, Bangalore'),
(12, '3456789023456789', 'Rupay', '2027-11-03', '110, Sector 5, Noida'),
(13, '4567890134567890', 'American Express', '2028-01-08', '909, Marine Drive, Mumbai'),
(14, '5678901245678901', 'Visa', '2025-08-24', '808, Velachery, Chennai'),
(15, '6789012356789012', 'MasterCard', '2026-03-11', '404, Gandhi Road, Surat'),
(16, '7890123467890123', 'Rupay', '2027-07-17', '204, Ashok Nagar, Hyderabad'),
(17, '8901234578901234', 'Visa', '2028-09-05', '706, Alkapuri, Vadodara'),
(18, '9012345689012345', 'Visa', '2025-04-30', '202, Rajarhat, Kolkata'),
(19, '1234567890123456', 'MasterCard', '2026-06-29', '101, Park Avenue, Chennai'),
(20, '2345678901234567', 'Rupay', '2027-12-15', '505, S.G. Highway, Ahmedabad'),
(21, '3456789012345678', 'Visa', '2025-05-21', '602, New Town, Kolkata'),
(22, '4567890123456789', 'American Express', '2028-02-12', '405, Greater Kailash, Delhi'),
(23, '5678901234567890', 'Visa', '2026-09-09', '909, Connaught Circle, New Delhi'),
(24, '6789012345678901', 'Rupay', '2027-01-28', '707, South Extension, Delhi'),
(25, '7890123456789012', 'MasterCard', '2028-10-14', '505, Whitefield, Bangalore');


SELECT * FROM User_Payment_Info;
