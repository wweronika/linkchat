CREATE TABLE `groups` (
	`group_id` int NOT NULL AUTO_INCREMENT,
	`title` TEXT NOT NULL,
	`last_message` DATETIME NOT NULL,
	PRIMARY KEY (`group_id`)
);

CREATE TABLE `user_group` (
	`group_id` int NOT NULL,
	`user_id` int NOT NULL
);

CREATE TABLE `users` (
	`user_id` int NOT NULL AUTO_INCREMENT,
	`login` TEXT NOT NULL,
	`salted_password` TEXT NOT NULL,
	`salt` TEXT NOT NULL,
	`email` TEXT NOT NULL,
	`is_active` bool NOT NULL DEFAULT '0',
	PRIMARY KEY (`user_id`)
);

CREATE TABLE `links` (
	`link_id` int NOT NULL AUTO_INCREMENT,
	`message_id` int NOT NULL,
	`date` DATETIME NOT NULL,
	PRIMARY KEY (`link_id`)
);

CREATE TABLE `messages` (
	`message_jd` int NOT NULL AUTO_INCREMENT,
	`sender_id` int NOT NULL,
	`group_id` int NOT NULL,
	`text` TEXT NOT NULL,
	`date` DATETIME NOT NULL,
	`is_link` bool NOT NULL DEFAULT '0',
	`parent_link_id` int,
	PRIMARY KEY (`message_jd`)
);

CREATE TABLE `tokens` (
	`user_id` int NOT NULL,
	`token` TEXT NOT NULL
);

CREATE TABLE `activation_links` (
	`token` TEXT NOT NULL,
	`date` DATETIME NOT NULL,
	`user_login` TEXT NOT NULL
);

ALTER TABLE `user_group` ADD CONSTRAINT `user_group_fk0` FOREIGN KEY (`group_id`) REFERENCES `groups`(`group_id`);

ALTER TABLE `user_group` ADD CONSTRAINT `user_group_fk1` FOREIGN KEY (`user_id`) REFERENCES `users`(`user_id`);

ALTER TABLE `links` ADD CONSTRAINT `links_fk0` FOREIGN KEY (`message_id`) REFERENCES `messages`(`message_jd`);

ALTER TABLE `messages` ADD CONSTRAINT `messages_fk0` FOREIGN KEY (`sender_id`) REFERENCES `users`(`user_id`);

ALTER TABLE `messages` ADD CONSTRAINT `messages_fk1` FOREIGN KEY (`group_id`) REFERENCES `groups`(`group_id`);

ALTER TABLE `messages` ADD CONSTRAINT `messages_fk2` FOREIGN KEY (`parent_link_id`) REFERENCES `links`(`link_id`);

ALTER TABLE `tokens` ADD CONSTRAINT `tokens_fk0` FOREIGN KEY (`user_id`) REFERENCES `users`(`user_id`);
