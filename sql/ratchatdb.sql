CREATE TABLE `ratchatdb`.`ratsite` ( 
    `id` INT NOT NULL AUTO_INCREMENT , 
    `time` DATETIME CURRENT_TIMESTAMP , 
    `is_outside` BOOLEAN NOT NULL , 
    `is_alive` BOOLEAN NOT NULL , 
    `location` VARCHAR(255) NOT NULL , 
    PRIMARY KEY (`id`)
) ENGINE = InnoDB;

CREATE TABLE `ratchatdb`.`ratevidence` ( 
    `id` INT NOT NULL AUTO_INCREMENT , 
    `time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP , 
    `droppings` BOOLEAN NOT NULL , 
    `chewed` BOOLEAN NOT NULL , 
    `location` VARCHAR(255) NOT NULL , 
    PRIMARY KEY (`id`)
) ENGINE = InnoDB;