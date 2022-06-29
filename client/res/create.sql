CREATE TABLE IF NOT EXISTS `profile` (
  `id` TEXT,
  `username` TEXT,
  `public_key` BLOB NOT NULL,
  `private_key` BLOB NOT NULL,
  `last_sync_at` TEXT
);

CREATE TABLE IF NOT EXISTS `gem` (
  `id` TEXT NOT NULL,
  `name` TEXT NOT NULL,
  `desc` TEXT NOT NULL,
  `sprite` BLOB NOT NULL,
  `created_by` TEXT NOT NULL,
  `created_for` TEXT NOT NULL,
  `created_at` TEXT NOT NULL,
  `obtained_at` TEXT NOT NULL,
  `offered` BOOLEAN NOT NULL DEFAULT 0,
  `payload` BLOB NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `wanted` (
  `gem` TEXT NOT NULL,
  PRIMARY KEY (`gem`)
);
