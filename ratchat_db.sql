
/* DATABASE FILE
  This file automatically creates the 'ratchatdb' 
  database, along with its associated tables.
  - Michael Koohang 
*/

/* DATABASE CREATION
  Creates the 'ratchat' database and makes
  it the active database.
  - Michael Koohang
*/
CREATE DATABASE IF NOT EXISTS `ratchat_db`;
USE `ratchat_db`;

/* TABLE CREATION - ratevidence
  Creates the 'ratevidence' table and
  its associated fields.
  - Michael Koohang
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
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* TABLE CREATION - ratsite
  Creates the 'ratsite' table and
  its associated fields.
  - Michael Koohang
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
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


