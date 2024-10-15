DELIMITER $$

CREATE FUNCTION CalculateDiscountedPrice(original_price DECIMAL(10,2), discount_percentage DECIMAL(5,2))
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE discounted_price DECIMAL(10,2);
    SET discounted_price = original_price - (original_price * discount_percentage / 100);
    RETURN discounted_price;
END$$

CREATE PROCEDURE ApplyPromotion(IN booking_id INT, IN promotion_id INT)
BEGIN
    DECLARE original_price DECIMAL(10,2);
    DECLARE discount_percentage DECIMAL(5,2);
    DECLARE final_price DECIMAL(10,2);

    SELECT amount INTO original_price
    FROM Payment_Transactions
    WHERE booking_id = booking_id;

    SELECT discount_percentage INTO discount_percentage
    FROM Promotions
    WHERE promotion_id = promotion_id;

    SET final_price = CalculateDiscountedPrice(original_price, discount_percentage);

    UPDATE Payment_Transactions
    SET amount = final_price
    WHERE booking_id = booking_id;
END$$