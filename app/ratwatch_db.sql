
CREATE DATABASE  IF NOT EXISTS `ratwatch_db`;
USE `ratwatch_db`;

DROP TABLE IF EXISTS `original_reports`;
CREATE TABLE `original_reports` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `image` varchar(255) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `lat` double DEFAULT NULL,
  `lon` double DEFAULT NULL,
  `type` varchar(45) DEFAULT NULL,
  `out_in` varchar(45) DEFAULT NULL,
  `dead_alive` varchar(45) DEFAULT NULL,
  `chew_drop_hole` varchar(45) DEFAULT NULL,
  `finished` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `altered_reports`;
CREATE TABLE `altered_reports` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `image` varchar(255) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `lat` double DEFAULT NULL,
  `lon` double DEFAULT NULL,
  `type` varchar(45) DEFAULT NULL,
  `out_in` varchar(45) DEFAULT NULL,
  `dead_alive` varchar(45) DEFAULT NULL,
  `chew_drop_hole` varchar(45) DEFAULT NULL,
  `finished` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
