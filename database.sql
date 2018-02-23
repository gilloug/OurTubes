/*CREATE THE USER*/
/* CREATE USER 'ourtubes' IDENTIFIED BY 'ourtubes';*/

/*CREATE THE DATABASE*/
DROP DATABASE IF EXISTS `OurTubes`;
CREATE DATABASE `OurTubes`;
USE `OurTubes`;

/*GIVE DATABASE ACCESS TO USER*/
GRANT ALL PRIVILEGES ON OurTubes.* TO `ourtubes`;

/*ERASE PREVIOUS TABLE*/
DROP TABLE IF EXISTS `Chans`;

/*CRATE CHANNELS TABLE*/
CREATE TABLE `Chans` (
  `_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `_name` varchar(45) DEFAULT NULL,
  `_publicPassword` varchar(200) DEFAULT NULL,
  `_privatePassword` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

LOCK TABLES `Chans` WRITE;

UNLOCK TABLES;

/*ERASE PREVIOUS TABLE*/
DROP TABLE IF EXISTS `Users`;

/*CRATE USERS TABLE*/
CREATE TABLE Users (
  _id BIGINT NOT NULL AUTO_INCREMENT,
  _email VARCHAR(45) NULL,
  _password VARCHAR(200) NULL,
  PRIMARY KEY (_id));

LOCK TABLES `Users` WRITE;

UNLOCK TABLES;

/*DELETE PREVIOUS TABLE*/
DROP TABLE IF EXISTS `PlayLists`;

/*CREATE PLAYLISTS TABLE*/
CREATE TABLE `PlayLists` (
  `_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `_Chanid` bigint(20) DEFAULT NULL,
  `_url` varchar(500) DEFAULT NULL,
  `_picture` varchar(500) DEFAULT NULL,
  `_title` varchar(500) DEFAULT NULL,
  `_likes` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`_id`),
  KEY `fk_Chanid` (`_Chanid`),
  CONSTRAINT `fk_Chanid` FOREIGN KEY (`_Chanid`) REFERENCES `Chans` (`_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `PlayLists` WRITE;

UNLOCK TABLES;


/*DELETE PREVIOUS TABLE*/
DROP TABLE IF EXISTS `Actions`;

/*CREATE ACTIONS TABLE*/
CREATE TABLE Actions (
  _id BIGINT NOT NULL AUTO_INCREMENT,
  _Userid BIGINT NULL,
  _Chanid BIGINT NULL,
  _url VARCHAR(500) NULL,
  _action INTEGER NULL,
  PRIMARY KEY (_id));

LOCK TABLES `Actions` WRITE;

UNLOCK TABLES;

/*HERE WE ARE GOING TO CREATE ALL THE PROCEDURES WE NEED*/

/*CREATE A CHANNEL*/
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `createChan`(
    IN p_name VARCHAR(45),
    IN p_publicPassword VARCHAR(200),
    IN p_privatePassword VARCHAR(200)
)
BEGIN
    if ( select exists (select 1 from Chans where _name = p_name) ) THEN
       select 'Chan already exist in table';
    ELSE
       insert into Chans
       (
            _name,
            _publicPassword,
            _privatePassword
       )
       values
       (
            p_name,
            p_publicPassword,
            p_privatePassword
       );
    END IF;
END$$
DELIMITER ;

/*DELETE A CHANNEL*/
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `deleteChan`(
    IN p_name VARCHAR(45),
    IN p_password VARCHAR(200)
)
BEGIN
    if ( select exists (select 1 from Chans where _name=p_name AND _privatePassword=p_password) ) THEN
       delete from PlayLists where _Chanid=(SELECT _id FROM Chans WHERE _name=p_name);
       delete from Chans where _name=p_name;
    ELSE
    select 'Chan does not exist in table';
    END IF;
END$$
DELIMITER ;

/*JOIN A CHANNEL AS AN ADMINISTRATOR*/
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `joinAsAdministrator`(
    IN p_name VARCHAR(45),
    IN p_password VARCHAR(200)
)
BEGIN
    select exists (select * from Chans where _name=p_name AND _privatePassword=p_password);
END$$
DELIMITER ;

/*JOIN A CHANNEL AS A GUEST*/
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `joinAsGuest`(
    IN p_name VARCHAR(45),
    IN p_password VARCHAR(200)
)
BEGIN
    select exists (select * from Chans where _name=p_name AND _publicPassword=p_password);
END$$
DELIMITER ;

/*ADD A MUSIC TO A PLAYLIST (CHANNEL)*/
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `addMusic`(
    IN p_name VARCHAR(500),
    IN p_url VARCHAR(500),
    IN p_picture VARCHAR(500),
    IN p_title VARCHAR(500)
)
BEGIN
    if (select exists (select 1 from PlayLists where _Chanid=(select _id from Chans where _name=p_name)\
 AND _url=p_url)) THEN
        select 'Music already in Chan';
    ELSE
        insert into PlayLists
        (
            _Chanid,
            _url,
            _picture,
            _likes,
            _title
        )
        values
        (
            (select _id from Chans where _name=p_name),
            p_url,
            p_picture,
            0,
            p_title
        );
    END IF;
END$$
DELIMITER ;

/*REMOVE A MUSIC FROM A PLAYLIST (CHANNEL)*/
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `removeMusic`(
    IN p_name VARCHAR(500),
    IN p_url VARCHAR(500)
)
BEGIN
    if (select exists (select 1 from PlayLists where _Chanid=(select _id from Chans where _name=p_name) AND _url=p_url)) THEN
       delete from PlayLists where _url=p_url AND _Chanid=(select _id from Chans where _name=p_name);
    ELSE
        select 'Music does not exist in Chan';
    END IF;
END$$
DELIMITER ;

/*UPVOTE A MUSIC*/
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `upMusic`(
    IN p_name VARCHAR(500),
    IN p_url VARCHAR(500)
)
BEGIN
    if (select exists (select 1 from PlayLists where _Chanid=(select _id from Chans where _name=p_name) AND _url=p_url)) THEN
    UPDATE PlayLists SET _likes=_likes+1 WHERE _url=p_url AND _Chanid=(select _id from Chans where _name=p_name);
    ELSE
        select 'Music does not exist in Chan';
    END IF;
END$$
DELIMITER ;

/*DOWNVOTE A MUSIC*/
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `downMusic`(
    IN p_name VARCHAR(500),
    IN p_url VARCHAR(500)
)
BEGIN
    if (select exists (select 1 from PlayLists where _Chanid=(select _id from Chans where _name=p_name) AND _url=p_url)) THEN
       UPDATE PlayLists SET _likes=_likes-1 WHERE _url=p_url AND _Chanid=(select _id from Chans where _name=p_name);
    ELSE
        select 'Music does not exist in Chan';
    END IF;
END$$
DELIMITER ;

/*DELETE MUSIC IF LIKES<0*/
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `checkMusic`(
    IN p_name VARCHAR(500),
    IN p_url VARCHAR(500)
)
BEGIN
    if (select exists (select _likes from PlayLists where _Chanid=(select _id from Chans where _name=p_name) AND _url=p_url AND _likes=-1)) THEN
       DELETE FROM PlayLists WHERE _url=p_url AND _Chanid=(select _id from Chans where _name=p_name);
    ELSE
        select 'Music is ok';
    END IF;
END$$
DELIMITER ;

/*GET ALL MUSICS FROM A PLAYLIST*/
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `getPlaylist`(
    IN p_name VARCHAR(500)
)
BEGIN
    select * from PlayLists Where _Chanid=(select _id from Chans where _name=p_name);
END$$
DELIMITER ;

/*GET ALL CHANS*/
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `getChans`(
)
BEGIN
    select * from Chans;
END$$
DELIMITER ;

/*ADD A USER*/
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `addUser`(
    IN p_email VARCHAR(500),
    IN p_password VARCHAR(500)
)
BEGIN
    if (select exists (select 1 from Users where _email=p_email)) THEN
        select 'User already Exist';
    ELSE
        insert into Users
        (
            _email,
            _password
        )
        values
	(
            p_email,
            p_password
        );
    END IF;
END$$
DELIMITER ;


/*GET A USER*/
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `getUser`(
    IN p_email VARCHAR(500),
    IN p_password VARCHAR(500)
)
BEGIN
       select 1 from Users where _email=p_email AND _password=p_password;
END$$
DELIMITER ;

/*REMOVE A USER*/
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `removeUser`(
    IN p_email VARCHAR(500),
    IN p_password VARCHAR(500)
)
BEGIN
    if (select exists (select 1 from Users where _email=p_email AND _password=p_password)) THEN
       delete from Users where _email=p_email AND _password=p_password;
    ELSE
        select 'User does not exist or password is invalid';
    END IF;
END$$
DELIMITER ;

/*ADD OR UPDATE AN ACTION*/
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `addAction`(
    IN p_email VARCHAR(500),
    IN p_url VARCHAR(500),
    IN p_name VARCHAR(500),
    IN p_action INTEGER
)
BEGIN
    if (select exists (select 1 from Actions where _Userid=(SELECT _id FROM Users WHERE _email=p_email) AND _Chanid=(SELECT _id FROM Chans WHERE _name=p_name) AND _url=p_url)) THEN
       if ((select _action from Actions where _Userid=(SELECT _id FROM Users WHERE _email=p_email) AND _Chanid=(SELECT _id FROM Chans WHERE _name=p_name) AND _url=p_url) > 0) THEN
           if (p_action > 0) THEN
               SELECT 'Error';
           ELSE
               UPDATE Actions SET _action=-1 WHERE _Userid=(SELECT _id FROM Users WHERE _email=p_email) AND _Chanid=(SELECT _id FROM Chans WHERE _name=p_name) AND _url=p_url;
           END IF;
       ELSE
           if (p_action < 0) THEN
               SELECT 'Error';
           ELSE
               UPDATE Actions SET _action=+1 WHERE _Userid=(SELECT _id FROM Users WHERE _email=p_email) AND _Chanid=(SELECT _id FROM Chans WHERE _name=p_name) AND _url=p_url;
           END IF;
       END IF;
    ELSE
        insert into Actions
        (
            _Userid,
            _Chanid,
            _url,
            _action
        )
        values
        (
            (SELECT _id FROM Users WHERE _email=p_email),
            (SELECT _id FROM Chans WHERE _name=p_name),
            p_url,
            p_action
        );
    END IF;
END$$
DELIMITER ;

/*BAAAAAAAAAAAAAAAAAAAAD TRICKS WHEN MUSIC IS PLAYED*/
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `playMusic`(
    IN p_name VARCHAR(500),
    IN p_url VARCHAR(500)
)
BEGIN
    if (select exists (select 1 from PlayLists where _Chanid=(select _id from Chans where _name=p_name) AND _url=p_url)) THEN
    UPDATE PlayLists SET _likes=99999 WHERE _url=p_url AND _Chanid=(select _id from Chans where _name=p_name);
    ELSE
        select 'Music does not exist in Chan';
    END IF;
END$$
DELIMITER ;
