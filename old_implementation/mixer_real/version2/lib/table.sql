CREATE mixer(
    "idmx" int(32) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    "source" varchar(32),
    "destination" varchar(32),
    "currencies" varchar(5),
    "amount" varchar(10),
    "confirmations" int(2),
    "blk" int(6),
    "time" datetime
);
