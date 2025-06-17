DELIMITER //

CREATE PROCEDURE AddDonation(
    IN donorName VARCHAR(100),
    IN resourceType VARCHAR(50),
    IN quantity INT
)
BEGIN
    INSERT INTO Donation (DonorName, ResourceType, Quantity, DonationDate)
    VALUES (donorName, resourceType, quantity, CURDATE());

    UPDATE Inventory
    SET QuantityAvailable = QuantityAvailable + quantity
    WHERE ItemName = resourceType;
END;
//

DELIMITER ;

