use MovieBookingSite;

CREATE TABLE Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    contact_number VARCHAR(15),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE User_Preferences (
    preference_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    favorite_genre VARCHAR(50),
    preferred_seat_type VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE User_Roles (
    role_id INT PRIMARY KEY AUTO_INCREMENT,
    role_name VARCHAR(50) NOT NULL
);

CREATE TABLE User_Payment_Info (
    payment_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    card_number VARCHAR(16),
    card_type VARCHAR(20),
    expiry_date DATE,
    billing_address VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Movies (
    movie_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(100) NOT NULL,
    genre VARCHAR(50),
    duration INT, -- Duration in minutes
    rating DECIMAL(2, 1), -- Average rating
    release_date DATE,
    director VARCHAR(50),
    language VARCHAR(20)
);

CREATE TABLE Shows (
    show_id INT PRIMARY KEY AUTO_INCREMENT,
    movie_id INT,
    theater_id INT,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    screen_number INT,
    FOREIGN KEY (movie_id) REFERENCES Movies(movie_id)
);

CREATE TABLE Theaters (
    theater_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    location VARCHAR(255),
    total_screens INT
);

CREATE TABLE Show_Schedule (
    schedule_id INT PRIMARY KEY AUTO_INCREMENT,
    show_id INT,
    date DATE,
    time TIME,
    theater_id INT,
    FOREIGN KEY (show_id) REFERENCES Shows(show_id),
    FOREIGN KEY (theater_id) REFERENCES Theaters(theater_id)
);

CREATE TABLE Bookings (
    booking_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    show_id INT,
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'Pending',
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (show_id) REFERENCES Shows(show_id)
);

CREATE TABLE Tickets (
    ticket_id INT PRIMARY KEY AUTO_INCREMENT,
    booking_id INT,
    seat_number VARCHAR(10),
    price DECIMAL(10, 2),
    FOREIGN KEY (booking_id) REFERENCES Bookings(booking_id)
);

CREATE TABLE Seats (
    seat_id INT PRIMARY KEY AUTO_INCREMENT,
    show_id INT,
    seat_number VARCHAR(10),
    status VARCHAR(20) DEFAULT 'Available',
    FOREIGN KEY (show_id) REFERENCES Shows(show_id)
);

CREATE TABLE Payment_Transactions (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    booking_id INT,
    amount DECIMAL(10, 2),
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    payment_status VARCHAR(20) DEFAULT 'Pending',
    FOREIGN KEY (booking_id) REFERENCES Bookings(booking_id)
);

CREATE TABLE Reviews (
    review_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    movie_id INT,
    rating DECIMAL(2, 1),
    comments TEXT,
    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (movie_id) REFERENCES Movies(movie_id)
);

CREATE TABLE Promotions (
    promotion_id INT PRIMARY KEY AUTO_INCREMENT,
    promotion_details VARCHAR(255),
    start_date DATE,
    end_date DATE,
    discount_percentage DECIMAL(5, 2)
);

CREATE TABLE Feedback (
    feedback_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    feedback_type VARCHAR(50),
    comments TEXT,
    feedback_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Movie_Ratings (
    movie_rating_id INT PRIMARY KEY AUTO_INCREMENT,
    movie_id INT,
    average_rating DECIMAL(2 , 1 ),
    total_votes INT,
    FOREIGN KEY (movie_id)
        REFERENCES Movies (movie_id)
);

SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE' AND TABLE_SCHEMA='moviebookingsite';
