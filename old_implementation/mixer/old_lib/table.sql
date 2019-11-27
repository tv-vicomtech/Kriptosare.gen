DROP TABLE IF EXISTS 'casino';
CREATE 'casino'(
    'idca' INT(32) NOT NULL AUTO_INCREMENT,
    'source' VARCHAR(32),
    'currencies' VARCHAR(5),
    'amount' VARCHAR(10),
    'confirmations' INT(2),
    'blk' INT(6),
    'time' DATETIME,
    
    PRIMARY KEY ('idca'),
);
