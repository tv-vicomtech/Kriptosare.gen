CREATE DATABASE IF NOT EXISTS `db`;
CREATE USER 'vicomtech'@'%' IDENTIFIED BY 'vicomtech';
GRANT ALL PRIVILEGES ON *.* TO 'vicomtech'@'%';
