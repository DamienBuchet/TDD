CREATE DATABASE IF NOT EXISTS `tdd` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `tdd`;

CREATE TABLE `books` (
  `id` int(11) NOT NULL,
  `isbn` varchar(255) NOT NULL,
  `title` varchar(255) NOT NULL,
  `author` varchar(255) NOT NULL,
  `publisher` varchar(255) NOT NULL,
  `format` varchar(255) NOT NULL,
  `available` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `members` (
  `id` int(11) NOT NULL,
  `member_id` int(11) NOT NULL,
  `code` varchar(255) NOT NULL,
  `firstname` varchar(255) NOT NULL,
  `lastname` varchar(255) NOT NULL,
  `birthdate` date NOT NULL,
  `gender` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


ALTER TABLE `books`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `members`
  ADD PRIMARY KEY (`id`);


ALTER TABLE `books`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `members`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
