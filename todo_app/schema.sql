DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS board;
DROP TABLE IF EXISTS card;
DROP TABLE IF EXISTS board_member;
DROP TABLE IF EXISTS card_executor;

CREATE TABLE user (
  id TEXT PRIMARY KEY NOT NULL,
  email TEXT NOT NULL,
  name TEXT NOT NULL,
  password TEXT NOT NULL,
  registered TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL,
  info TEXT DEFAULT '' NOT NULL
);

CREATE TABLE board (
  id TEXT PRIMARY KEY NOT NULL,
  owner_id TEXT NOT NULL,
  title TEXT NOT NULL,
  created TEXT NOT NULL,
  FOREIGN KEY (owner_id)
    REFERENCES user (id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);

CREATE TABLE card (
  id TEXT PRIMARY KEY NOT NULL,
  board_id TEXT NOT NULL,
  owner_id TEXT NOT NULL,
  created TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL,
  status TEXT NOT NULL,
  importance TEXT NOT NULL,
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  FOREIGN KEY (board_id)
    REFERENCES board (id)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY (owner_id)
    REFERENCES user (id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);

CREATE TABLE board_member (
  user_id TEXT NOT NULL,
  board_id TEXT NOT NULL,
  PRIMARY KEY (user_id, board_id),
  FOREIGN KEY (user_id)
    REFERENCES user (id)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY (board_id)
    REFERENCES board (id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);

CREATE TABLE card_executor (
  user_id TEXT NOT NULL,
  card_id TEXT NOT NULL,
  PRIMARY KEY (user_id, card_id),
  FOREIGN KEY (user_id)
    REFERENCES user (id)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY (card_id)
    REFERENCES card (id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);