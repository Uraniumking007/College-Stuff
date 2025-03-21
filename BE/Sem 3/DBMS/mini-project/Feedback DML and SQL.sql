INSERT INTO Reviews (user_id, movie_id, rating, comments, review_date) VALUES
(1, 1, 4.5, 'Great movie with an excellent storyline!', '2024-09-15 10:30:00'),
(2, 2, 3.0, 'Average movie, could have been better.', '2024-09-16 11:00:00'),
(3, 3, 5.0, 'Absolutely loved the performance!', '2024-09-17 12:15:00'),
(4, 4, 2.0, 'Not my cup of tea. Lacked depth.', '2024-09-18 13:30:00'),
(5, 5, 4.0, 'Visually stunning and engaging.', '2024-09-19 14:00:00'),
(6, 6, 3.5, 'Good movie, but a bit predictable.', '2024-09-20 15:45:00'),
(7, 7, 4.5, 'Loved the plot twists!', '2024-09-21 16:30:00'),
(8, 8, 2.5, 'Had high hopes, but was disappointed.', '2024-09-22 17:00:00'),
(9, 9, 4.0, 'Worth watching for sure.', '2024-09-23 18:00:00'),
(10, 10, 5.0, 'Brilliant direction and acting.', '2024-09-24 19:15:00'),
(11, 11, 3.5, 'A decent movie with good pacing.', '2024-09-25 20:00:00'),
(12, 12, 4.0, 'Very enjoyable, would watch again.', '2024-09-26 21:00:00'),
(13, 13, 2.0, 'The movie dragged a lot.', '2024-09-27 22:00:00'),
(14, 14, 4.5, 'Loved every second of it.', '2024-09-28 23:00:00'),
(15, 15, 3.0, 'Good, but could use more character development.', '2024-09-29 10:00:00'),
(16, 16, 4.0, 'Great direction and visual effects.', '2024-09-30 11:00:00'),
(17, 17, 5.0, 'Best movie I have seen this year!', '2024-10-01 12:15:00'),
(18, 18, 3.0, 'Mediocre at best.', '2024-10-02 13:30:00'),
(19, 19, 4.5, 'Great casting, thoroughly enjoyed it.', '2024-10-03 14:00:00'),
(20, 20, 2.5, 'Not as good as expected.', '2024-10-04 15:45:00'),
(21, 21, 5.0, 'An amazing cinematic experience.', '2024-10-05 16:30:00'),
(22, 22, 3.0, 'A bit slow but good overall.', '2024-10-06 17:00:00'),
(23, 23, 4.0, 'Entertaining from start to finish.', '2024-10-07 18:00:00'),
(24, 24, 5.0, 'Masterpiece! Must watch.', '2024-10-08 19:15:00'),
(25, 25, 2.5, 'Could have been more engaging.', '2024-10-09 20:00:00');


SELECT * FROM Reviews;

INSERT INTO Promotions (promotion_details, start_date, end_date, discount_percentage) VALUES
('Diwali Special Discount', '2024-10-20', '2024-10-31', 15.00),
('New Year Bash Offer', '2024-12-25', '2025-01-01', 20.00),
('Republic Day Sale', '2025-01-20', '2025-01-27', 10.00),
('Valentine\'s Day Special', '2025-02-10', '2025-02-15', 12.50),
('Summer Blockbuster Sale', '2025-04-01', '2025-04-10', 18.00),
('Monsoon Madness', '2025-07-01', '2025-07-15', 20.00),
('Raksha Bandhan Special', '2025-08-20', '2025-08-25', 15.00),
('Ganesh Chaturthi Special', '2025-09-01', '2025-09-10', 12.00),
('Navratri Festival Discount', '2025-09-25', '2025-10-05', 10.50),
('Dussehra Dhamaka', '2025-10-15', '2025-10-22', 16.00),
('Christmas Carnival', '2024-12-20', '2024-12-26', 14.50),
('Eid Mubarak Offer', '2025-06-10', '2025-06-17', 18.00),
('Lohri Fest Discount', '2025-01-10', '2025-01-13', 12.00),
('Independence Day Sale', '2025-08-10', '2025-08-16', 10.00),
('Holi Hai Offer', '2025-03-01', '2025-03-10', 20.00),
('Baisakhi Fest Offer', '2025-04-12', '2025-04-15', 12.00),
('Karva Chauth Special', '2025-11-01', '2025-11-05', 15.50),
('Children\'s Day Discount', '2025-11-10', '2025-11-14', 10.00),
('Bhai Dooj Offer', '2025-11-15', '2025-11-20', 16.00),
('Pongal Fest Discount', '2025-01-10', '2025-01-16', 14.00),
('Onam Fest Discount', '2025-08-18', '2025-08-24', 11.00),
('Teacher\'s Day Special', '2025-09-01', '2025-09-07', 10.50),
('Mahashivratri Offer', '2025-02-12', '2025-02-18', 12.50),
('Easter Weekend Offer', '2025-04-10', '2025-04-13', 14.50),
('Christmas Eve Special', '2024-12-24', '2024-12-25', 15.00);

TRUNCATE TABLE REVIEWS;
SELECT * FROM Promotions;

INSERT INTO Feedback (user_id, feedback_type, comments, feedback_date) VALUES
(1, 'Complaint', 'The movie started late.', '2024-09-20 10:00:00'),
(2, 'Compliment', 'The seating was very comfortable.', '2024-09-21 11:00:00'),
(3, 'Suggestion', 'Would be nice to have more snacks options.', '2024-09-22 12:15:00'),
(4, 'Complaint', 'The sound system was not clear.', '2024-09-23 13:30:00'),
(5, 'Compliment', 'Great customer service!', '2024-09-24 14:00:00'),
(6, 'Suggestion', 'Need more showtimes for popular movies.', '2024-09-25 15:45:00'),
(7, 'Complaint', 'Seats were uncomfortable.', '2024-09-26 16:30:00'),
(8, 'Compliment', 'The experience was amazing!', '2024-09-27 17:00:00'),
(9, 'Suggestion', 'Better air conditioning would be nice.', '2024-09-28 18:00:00'),
(10, 'Complaint', 'The popcorn was too expensive.', '2024-09-29 19:15:00'),
(11, 'Compliment', 'Really loved the ambiance.', '2024-09-30 20:00:00'),
(12, 'Suggestion', 'More legroom would be great.', '2024-10-01 21:00:00'),
(13, 'Complaint', 'The screen had a flicker at times.', '2024-10-02 22:00:00'),
(14, 'Compliment', 'The staff was very helpful.', '2024-10-03 23:00:00'),
(15, 'Suggestion', 'Could improve the parking facilities.', '2024-10-04 10:00:00'),
(16, 'Complaint', 'The AC was too cold in the theater.', '2024-10-05 11:00:00'),
(17, 'Compliment', 'Great sound system.', '2024-10-06 12:15:00'),
(18, 'Suggestion', 'More variety in beverages.', '2024-10-07 13:30:00'),
(19, 'Complaint', 'The queue for tickets was too long.', '2024-10-08 14:00:00'),
(20, 'Compliment', 'The theater was very clean.', '2024-10-09 15:45:00'),
(21, 'Suggestion', 'Please add recliner seats.', '2024-10-10 16:30:00'),
(22, 'Complaint', 'Parking was difficult to find.', '2024-10-11 17:00:00'),
(23, 'Compliment', 'The ticketing process was smooth.', '2024-10-12 18:00:00'),
(24, 'Suggestion', 'More shows during weekends would be nice.', '2024-10-13 19:15:00'),
(25, 'Complaint', 'The movie was interrupted multiple times.', '2024-10-14 20:00:00');

SELECT * FROM Feedback;

INSERT INTO Movie_Ratings (movie_id, average_rating, total_votes) VALUES
(1, 4.5, 250),
(2, 3.0, 150),
(3, 5.0, 300),
(4, 2.0, 75),
(5, 4.0, 200),
(6, 3.5, 180),
(7, 4.5, 220),
(8, 2.5, 100),
(9, 4.0, 210),
(10, 5.0, 320),
(11, 3.5, 190),
(12, 4.0, 230),
(13, 2.0, 90),
(14, 4.5, 270),
(15, 3.0, 130),
(16, 4.0, 200),
(17, 5.0, 350),
(18, 3.0, 140),
(19, 4.5, 260),
(20, 2.5, 120),
(21, 5.0, 300),
(22, 3.0, 160),
(23, 4.0, 240),
(24, 5.0, 310),
(25, 2.5, 110);

SELECT * FROM Movie_Ratings;