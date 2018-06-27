
/* ratwatch_db.sql
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
DROP TABLE IF EXISTS `rat_evidence`;
CREATE TABLE `rat_evidence` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `address` varchar(255) DEFAULT NULL,
  `lat` double DEFAULT NULL,
  `lon` double DEFAULT NULL,
  `droppings` tinyint(1) DEFAULT NULL,
  `chewed` tinyint(1) DEFAULT NULL,
  `image` varchar(100) DEFAULT NULL,
  `finished` tinyint(1) DEFAULT '0',
  `restarted` tinyint(1) DEFAULT '0',
  `made_mistake` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* TABLE CREATION - ratsite
  Creates the 'ratsite' table and
  its associated fields.
*/
DROP TABLE IF EXISTS `rat_sightings`;
CREATE TABLE `rat_sightings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `address` varchar(255) DEFAULT NULL,
  `lat` double DEFAULT NULL,
  `lon` double DEFAULT NULL,
  `is_outside` tinyint(1) DEFAULT NULL,
  `is_alive` tinyint(1) DEFAULT NULL,
  `image` varchar(100) DEFAULT NULL,
  `finished` tinyint(1) DEFAULT '0',
  `restarted` tinyint(1) DEFAULT '0',
  `made_mistake` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


