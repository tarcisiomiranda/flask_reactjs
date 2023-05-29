CREATE TABLE IF NOT EXISTS `vasco`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `email` text,
  `mobile` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `birth_date` date DEFAULT NULL
  UNIQUE INDEX `is_UNIQUE` (`id` ASC) VISIBLE)
ENGINE = InnoDB;

INSERT INTO `users` (`id`, `name`, `email`, `mobile`, `birth_date`) VALUES
(1, 'Teixeira Alex', 'vasco@da.gama', '+55123456789', '2023-05-17'),
(2, 'Pac Gabriel', 'vasco@da.gama', '+55123456789', '2023-05-17');
