CREATE DATABASE IF NOT EXISTS vasco;

CREATE TABLE IF NOT EXISTS `vasco`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `email` text,
  `mobile` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `birth_date` date DEFAULT NULL,
  PRIMARY KEY (`id`)
)
ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `vasco`.`users` (`name`, `email`, `mobile`, `birth_date`) VALUES
('Teixeira Alex', 'vasco@da.gama', '+55123456789', '2023-05-29'),
('Pac Gabriel', 'vasco@da.gama', '+55123456789', '2023-05-29');

GRANT ALL PRIVILEGES ON `vasco`.* TO 'python'@'%';
GRANT ALL PRIVILEGES ON `vasco`.* TO 'root'@'localhost';
GRANT ALL PRIVILEGES ON `vasco`.* TO 'root'@'127.0.0.1';
