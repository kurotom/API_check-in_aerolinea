CREATE TABLE `airplane` (
	`airplane_id` INT(11),
	`name` varchar(255) DEFAULT NULL,
	PRIMARY KEY (`airplane_id`)
);

CREATE TABLE `boarding_pass` (
  `boarding_pass_id` int(11),
  `purchase_id` int DEFAULT NULL,
  `passenger_id` int DEFAULT NULL,
  `seat_type_id` int DEFAULT NULL,
  `seat_id` int DEFAULT NULL,
  `flight_id` int DEFAULT NULL,
  PRIMARY KEY (`boarding_pass_id`)
);

CREATE TABLE `flight` (
  `flight_id` int,
  `takeoff_date_time` int DEFAULT NULL,
  `takeoff_airport` varchar(255) DEFAULT NULL,
  `landing_date_time` int DEFAULT NULL,
  `landing_airport` varchar(255) DEFAULT NULL,
  `airplane_id` int DEFAULT NULL,
  PRIMARY KEY (`flight_id`)
);

CREATE TABLE `passenger` (
  `passenger_id` int,
  `dni` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `age` int DEFAULT NULL,
  `country` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`passenger_id`)
);

CREATE TABLE `purchase` (
  `purchase_id` int,
  `purchase_date` int DEFAULT NULL,
  PRIMARY KEY (`purchase_id`)
);

CREATE TABLE `seat` (
  `seat_id` int,
  `seat_column` varchar(2) DEFAULT NULL,
  `seat_row` int DEFAULT NULL,
  `seat_type_id` int DEFAULT NULL,
  `airplane_id` int DEFAULT NULL,
  PRIMARY KEY (`seat_id`)
);

CREATE TABLE `seat_type` (
  `seat_type_id` int,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`seat_type_id`)
);
