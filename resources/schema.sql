CREATE TABLE IF NOT EXISTS `members` (
    `member_id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `name` varchar(255) NOT NULL,
    UNIQUE(`name`)
);

CREATE TABLE IF NOT EXISTS `disclosures` (
    `disclosures_id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `filing_year` int(12) NOT NULL,
    `filing` varchar(255) NOT NULL,
    `link` varchar(255) NOT NULL,
    `member_id` INTEGER NOT NULL,
    FOREIGN KEY (`member_id`) REFERENCES `members`(`member_id`)
);
