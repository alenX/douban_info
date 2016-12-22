create table douban_book
(id INT(32) PRIMARY KEY AUTO_INCREMENT,name VARCHAR(64),
  author VARCHAR(32),county varchar(32),translator VARCHAR(32),press VARCHAR(32),
  data_str VARCHAR(32),price DECIMAL(6,2),socre FLOAT,description TEXT,image VARCHAR(128));


CREATE table douban_book_tag(id INT(32) PRIMARY KEY AUTO_INCREMENT,tag_name VARCHAR(32))