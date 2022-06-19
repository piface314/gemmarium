CREATE TABLE IF NOT EXISTS user (
  username TEXT NOT NULL,
  public_key BLOB NOT NULL,
  PRIMARY KEY (username)
);
