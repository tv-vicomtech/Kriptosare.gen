DROP TABLE IF EXISTS 'pool';
CREATE 'pool'(
    'idpo' INT(32) NOT NULL AUTO_INCREMENT,
    'source' VARCHAR(32),
    'currencies' VARCHAR(5),
    'amount' VARCHAR(10),
    'confirmations' INT(2),
    'blk' INT(6),
    'time' DATETIME,
    
    PRIMARY KEY ('idpo'),
);

CREATE 'gen'(
    'idgen' INT(32) NOT NULL AUTO_INCREMENT,
    'tx_rec' INT(32),
    'amount_rec' VARCHAR(5),
    'tx_sent' INT(10),
    'amount_sent' VARCHAR(2),
    'balance' VARCHAR(6),
    'unique' INT(6),
    'sibling' INT(6),
    'ending' INT(6),
    
    PRIMARY KEY ('idgen'),
);
