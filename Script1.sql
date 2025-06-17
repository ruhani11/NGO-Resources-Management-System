CREATE TABLE Volunteer (
    VolunteerID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100),
    Email VARCHAR(100) UNIQUE,
    Phone VARCHAR(15),
    Skills TEXT,
    Availability BOOLEAN
);

CREATE TABLE Donation (
    DonationID INT PRIMARY KEY AUTO_INCREMENT,
    DonorName VARCHAR(100),
    ResourceType VARCHAR(50),
    Quantity INT,
    DonationDate DATE
);

CREATE TABLE Inventory (
    ItemID INT PRIMARY KEY AUTO_INCREMENT,
    ItemName VARCHAR(100),
    QuantityAvailable INT
);

CREATE TABLE ChildProfile (
    ChildID INT PRIMARY KEY AUTO_INCREMENT,
    Age INT,
    Gender VARCHAR(10),
    SupportType VARCHAR(100),
    Comments TEXT
);

CREATE TABLE Event (
    EventID INT PRIMARY KEY AUTO_INCREMENT,
    EventName VARCHAR(100),
    EventDate DATE,
    Description TEXT
);

CREATE TABLE Participation (
    ParticipationID INT PRIMARY KEY AUTO_INCREMENT,
    EventID INT,
    VolunteerID INT,
    FOREIGN KEY (EventID) REFERENCES Event(EventID),
    FOREIGN KEY (VolunteerID) REFERENCES Volunteer(VolunteerID)
);
