
/* DATABASE FILE
  This file automatically creates the 'ratwatch_db' 
  database, along with its associated tables.
*/

/* DATABASE CREATION
  Creates the 'ratwatch_db' database and makes
  it the active database.
*/
CREATE DATABASE IF NOT EXISTS `ratwatch_db`;
USE `ratwatch_db`;

/* TABLE CREATION - ratevidence
  Creates the 'ratevidence' table and
  its associated fields.
*/
DROP TABLE IF EXISTS `ratevidence`;
CREATE TABLE `ratevidence` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `droppings` tinyint(1) NOT NULL,
  `chewed` tinyint(1) NOT NULL,
  `street` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL,
  `zipcode` varchar(255) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* TABLE CREATION - ratsite
  Creates the 'ratsite' table and
  its associated fields.
*/
DROP TABLE IF EXISTS `ratsite`;
CREATE TABLE `ratsite` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `is_outside` tinyint(1) NOT NULL,
  `is_alive` tinyint(1) NOT NULL,
  `street` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL,
  `zipcode` varchar(255) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


