CREATE DATABASE appstore_spider;

USE appstore_spider;

CREATE TABLE apps (
    `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
    `display_name` varchar(128) DEFAULT NULL,
    `package_name` varchar(32) DEFAULT NULL,
    `keyword` varchar(64) DEFAULT NULL,
    `dlcount` varchar(32) DEFAULT NULL,
    `comment_count` varchar(16) DEFAULT NULL,
    `category` varchar(256) DEFAULT NULL,
    `update_time` varchar(32) DEFAULT NULL,
    `version` varchar(32) DEFAULT NULL,
    `ranking` int(11) NOT NULL,
    `rating` int(11) NOT NULL,
    `time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
