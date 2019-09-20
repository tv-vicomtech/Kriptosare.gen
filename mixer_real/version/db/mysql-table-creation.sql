CREATE TABLE IF NOT EXISTS accounts
 (account_id int NOT NULL auto_increment,
  input_address varchar(35) NOT NULL,
  required_confirmations int NOT NULL,
  active_flag char(1) NOT NULL DEFAULT 'Y',
  secret_mixing_key char(64) NOT NULL,
  created_datetime datetime NOT NULL,
  primary key (account_id),
  unique (input_address),
  unique (secret_mixing_key)
 );
CREATE TABLE IF NOT EXISTS output_addresses
 (output_address_id int NOT NULL auto_increment,
  account_id int NOT NULL,
  output_address varchar(35) NOT NULL,
  primary key (output_address_id),
  foreign key (account_id) references accounts(account_id)
 );
CREATE TABLE IF NOT EXISTS payments
 (payment_id int NOT NULL auto_increment,
  output_address_id int NOT NULL,
  amount_gross decimal(16,8) NOT NULL,
  amount_net decimal(16,8) NOT NULL,
  transaction_id char(64) NULL,
  created_datetime datetime NOT NULL,
  payment_datetime datetime NOT NULL,
  primary key (payment_id),
  foreign key (output_address_id) references output_addresses(output_address_id)
 );

