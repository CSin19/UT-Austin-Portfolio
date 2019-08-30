/*
-- VENUES TABLE DEFINITION--
DROP TABLE IF EXISTS Venues;
CREATE TABLE IF NOT EXISTS Venues 
                        (VenueId INT PRIMARY KEY AUTO_INCREMENT, 
                        VenueName varchar(15) NOT NULL,
                        VenueZipcode varchar(5) NOT NULL,
                        VenueAddress varchar(30) NOT NULL,
                        VenueOpeningTime varchar(4) NOT NULL,
                        VenueClosingTime varchar(4) NOT NULL,
                        VenueSports varchar(15),
                        CHECK (LENGTH(VenueZipcode)=5 AND LENGTH(VenueName)<=15 AND LENGTH(VenueAddress)<=30));
INSERT INTO Venues(VenueName, VenueZipcode, VenueAddress, VenueOpeningTime, VenueClosingTime, VenueSports) 
                      VALUES("Venue 1", "78705", "26th Street", "0900", "1800", "Football");
INSERT INTO Venues(VenueName, VenueZipcode, VenueAddress, VenueOpeningTime, VenueClosingTime, VenueSports) 
                      VALUES("Venue 2", "78706", "27th Street", "0900", "1700", "Basketball");
INSERT INTO Venues(VenueName, VenueZipcode, VenueAddress, VenueOpeningTime, VenueClosingTime, VenueSports) 
                      VALUES("Venue 3", "78707", "28th Street", "0900", "1600", "Tennis");
INSERT INTO Venues(VenueName, VenueZipcode, VenueAddress, VenueOpeningTime, VenueClosingTime, VenueSports) 
                      VALUES("Venue 4", "78708", "29th Street", "0900", "1500", "Swimming");
INSERT INTO Venues(VenueName, VenueZipcode, VenueAddress, VenueOpeningTime, VenueClosingTime, VenueSports) 
                      VALUES("Venue 5", "78709", "30th Street", "0900", "1400", "Cricket");
INSERT INTO Venues(VenueName, VenueZipcode, VenueAddress, VenueOpeningTime, VenueClosingTime, VenueSports) 
                      VALUES("Venue 6", "78700", "34th Street", "1000", "1800", "Football");
INSERT INTO Venues(VenueName, VenueZipcode, VenueAddress, VenueOpeningTime, VenueClosingTime, VenueSports) 
                      VALUES("Venue 7", "78701", "35th Street", "1100", "1800", "Basketball");
INSERT INTO Venues(VenueName, VenueZipcode, VenueAddress, VenueOpeningTime, VenueClosingTime, VenueSports) 
                      VALUES("Venue 8", "78702", "36th Street", "1200", "1800", "Tennis");
INSERT INTO Venues(VenueName, VenueZipcode, VenueAddress, VenueOpeningTime, VenueClosingTime, VenueSports) 
                      VALUES("Venue 9", "78703", "37th Street", "1300", "1800", "Swimming");
INSERT INTO Venues(VenueName, VenueZipcode, VenueAddress, VenueOpeningTime, VenueClosingTime, VenueSports) 
                      VALUES("Venue 10", "78704", "38th Street", "1200", "1700", "Cricket");

-- USERS TABLE DEFINITION ---
DROP TABLE IF EXISTS Users;
CREATE TABLE IF NOT EXISTS Users 
                        (uId INT PRIMARY KEY AUTO_INCREMENT, 
						 uName varchar(20) NOT NULL,
						 uPhone varchar(10) NOT NULL,
						 uEmail varchar(30) NOT NULL,
						 uPassword varchar(15) NOT NULL,
						 uZipcode varchar(5) NOT NULL,
						 admin varchar(5) NOT NULL);
INSERT INTO Users(uName, uPhone, uEmail, uPassword, uZipcode ,admin) 
                      VALUES("Chetna", 37576787, "c@gmail", "Hello", 78709, "True");
					
-- EVENTS TABLE DEFINITION --
DROP TABLE IF EXISTS Events;
CREATE TABLE IF NOT EXISTS Events
						(EventId INT PRIMARY KEY AUTO_INCREMENT, 
                        EventName varchar(30) NOT NULL,
                        EventDate varchar(10) NOT NULL,
                        EventSport varchar(15) NOT NULL,
                        EventTeamSize INT NOT NULL,
                        EventSpotsLeft INT NOT NULL,
                        EventDesc varchar(30),
                        VenueId INT NOT NULL,
                        EventHost INT NOT NULL,
                        EventStartTime varchar(4) NOT NULL,
                        EventEndTime varchar(4) NOT NULL,
                        FOREIGN KEY (EventHost) references Users(uId),
                        FOREIGN KEY (VenueId) REFERENCES Venues(VenueId));
INSERT INTO Events(EventName,EventDate, EventSport, EventTeamSize, 
                    EventSpotsLeft, EventDesc, VenueId, EventHost, EventStartTime, EventEndTime) 
                          VALUES('Event 1', '2019-03-02', 'Baseball', 10,9,'American',1,1,'1600', '1800');

-- EVENTS TABLE DEFINITION --
DROP TABLE IF EXISTS User_Events;
CREATE TABLE IF NOT EXISTS User_Events
						(EventId INT NOT NULL,
                         uId INT NOT NULL,
                         FOREIGN KEY (EventId) REFERENCES Events(EventId) ON DELETE CASCADE, 
                         FOREIGN KEY (uId) REFERENCES Users(uId) ON DELETE CASCADE);
INSERT INTO User_Events(EventId, uId)
                          VALUES(1, 1);

GRANT ALL PRIVILEGES ON *.* TO 'livestrong19'@'cloudsqlproxy~67.78.117.195' IDENTIFIED BY 'livestrong19';
GRANT ALL PRIVILEGES ON *.* TO 'livestrong19'@'localhost' IDENTIFIED BY 'livestrong19';

INSERT INTO Venues(VenueName, VenueZipcode, VenueAddress, VenueOpeningTime, VenueClosingTime, VenueSports) 
                      VALUES("Venue 11", "78710", "39th Street", "0900", "1600", "Football");
INSERT INTO Users(uname, uphone, uemail, upassword, uZipcode ,admin) 
VALUES("Kyle", 23456, "d@gmail", "Why", 78705, "False");
COMMIT;
DELETE FROM Venues WHERE VenueName = "Venue 12";
INSERT INTO Users(uname, uphone, uemail, upassword, uZipcode ,admin) 
VALUES("Bob", 85786, "s@gmail", "Dude", 98690, "False");
COMMIT;
INSERT INTO Users(uname, uphone, uemail, upassword, uZipcode ,admin) 
VALUES("Mary", 85744, "m@gmail", "Life", 92290, "False");
COMMIT;
SELECT * FROM Events;
INSERT INTO Events(EventName,EventDate, EventSport, EventTeamSize, 
                    EventSpotsLeft, EventDesc, VenueId, EventHost, EventStartTime, EventEndTime) 
VALUES('Event 1', '2019-03-02', 'baseball', 10,9,'bring the ball',1, 7, '1600', '1800');
COMMIT;

INSERT INTO Events(EventName,EventDate, EventSport, EventTeamSize, 
                    EventSpotsLeft, EventDesc, VenueId, EventHost, EventStartTime, EventEndTime) 
VALUES('Event 2', '2019-03-02', 'baseball', 10,9,'bring the ball',1, 7, '1600', '1800');
INSERT INTO Events(EventName,EventDate, EventSport, EventTeamSize, 
                    EventSpotsLeft, EventDesc, VenueId, EventHost, EventStartTime, EventEndTime) 
VALUES('Event 3', '2019-03-02', 'baseball', 10,9,'bring the ball',1, 7, '1600', '1800');*/
select * from User_Events;