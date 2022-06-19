CREATE TABLE IF NOT EXISTS quota (
  username TEXT NOT NULL,
  last_request_at TEXT NOT NULL,
  PRIMARY KEY (username)
);
