-- Insert a new user (user registration)
INSERT INTO
    Users (name, email, password, contact_number)
VALUES
    (
        'Amit Kumar',
        'amit.kumar@example.com',
        'password123',
        '9876543210'
    );

-- List all movies
SELECT
    movie_id,
    title,
    genre,
    duration,
    release_date,
    rating,
    director,
    language
FROM
    Movies;

-- Shows available for a specific movie
SELECT
    Shows.show_id,
    Shows.start_time,
    Shows.end_time,
    Theaters.name AS theater_name,
    Theaters.location,
    Shows.screen_number
FROM
    Shows
    JOIN Theaters ON Shows.theater_id = Theaters.theater_id
WHERE
    Shows.movie_id = 1;

-- Book a Ticket
INSERT INTO
    Bookings (user_id, show_id, booking_date, status)
VALUES
    (1, 1, NOW (), 'Confirmed');

UPDATE Seats
SET
    status = 'Booked'
WHERE
    show_id = 1
    AND seat_number = 'A1';

INSERT INTO
    Tickets (booking_id, seat_number, price)
VALUES
    (LAST_INSERT_ID (), 'A1', 250.00);

INSERT INTO
    Payment_Transactions (booking_id, amount, payment_date, payment_status)
VALUES
    (LAST_INSERT_ID (), 250.00, NOW (), 'Completed');

-- View bookings for a specific user
SELECT
    u.user_id,
    u.name AS user_name,
    u.email AS user_email,
    b.booking_id,
    m.title AS movie_title,
    s.start_time AS show_start_time,
    t.name AS theater_name,
    tk.seat_number,
    b.status AS booking_status,
    pt.amount AS payment_amount,
    pt.payment_status
FROM
    Users u
    JOIN Bookings b ON u.user_id = b.user_id
    JOIN Shows s ON b.show_id = s.show_id
    JOIN Movies m ON s.movie_id = m.movie_id
    JOIN Theaters t ON s.theater_id = t.theater_id
    JOIN Tickets tk ON b.booking_id = tk.booking_id
    JOIN Payment_Transactions pt ON b.booking_id = pt.booking_id
WHERE
    u.user_id = 22;

-- Booking Cancellation
UPDATE Bookings
SET
    status = 'Cancelled'
WHERE
    booking_id = 1;

UPDATE Seats
SET
    status = 'Available'
WHERE
    seat_number = 'A1'
    AND show_id = 1;

UPDATE Payment_Transactions
SET
    payment_status = 'Refunded'
WHERE
    booking_id = 1;

-- Insert feedback and Review
INSERT INTO
    Feedback (user_id, feedback_type, comments, feedback_date)
VALUES
    (
        1,
        'Compliment',
        'Great movie experience!',
        NOW ()
    );

INSERT INTO
    Reviews (user_id, movie_id, rating, comments, review_date)
VALUES
    (
        1,
        1,
        4.5,
        'Amazing storyline and acting!',
        NOW ()
    );

-- List active promotions
SELECT
    promotion_id,
    promotion_details,
    discount_percentage,
    start_date,
    end_date
FROM
    Promotions
WHERE
    DATE ("2024-10-25") BETWEEN start_date AND end_date;

-- Display all users and their preferences
SELECT
    u.user_id,
    u.name,
    u.email,
    p.favorite_genre,
    p.preferred_seat_type
FROM
    Users u
    JOIN User_Preferences p ON u.user_id = p.user_id;

-- Display all movies and their ratings
SELECT
    m.movie_id,
    m.title,
    m.genre,
    mr.average_rating,
    mr.total_votes
FROM
    Movies m
    JOIN Movie_Ratings mr ON m.movie_id = mr.movie_id;

-- Display available seats for a specific show
SELECT
    seat_number,
    status
FROM
    Seats
WHERE
    show_id = 5
    AND status = 'Available';

-- Display all bookings along with user details
SELECT
    b.booking_id,
    u.name,
    u.email,
    m.title,
    t.name AS theater_name,
    s.start_time,
    tk.seat_number,
    b.status
FROM
    Bookings b
    JOIN Users u ON b.user_id = u.user_id
    JOIN Shows s ON b.show_id = s.show_id
    JOIN Movies m ON s.movie_id = m.movie_id
    JOIN Theaters t ON s.theater_id = t.theater_id
    JOIN Tickets tk ON b.booking_id = tk.booking_id;

-- Calculate discount
SELECT
    CalculateDiscountedPrice (500.00, 15.00);

-- Apply promotion
CALL ApplyPromotion (1, 2); -- ApplyPromotion(booking_id, promotion_id)