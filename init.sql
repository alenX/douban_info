CREATE TABLE douban_book
(
  id          INT(32) PRIMARY KEY AUTO_INCREMENT,
  name        VARCHAR(64),
  author      VARCHAR(128),
  county      VARCHAR(32),
  translator  VARCHAR(32),
  press       VARCHAR(32),
  data_str    VARCHAR(32),
  price       VARCHAR(16),
  socre       FLOAT,
  description TEXT,
  image       VARCHAR(128)
);
CREATE TABLE douban_book_tag (
  id       INT(32) PRIMARY KEY AUTO_INCREMENT,
  tag_name VARCHAR(32)
)