CREATE TABLE IF NOT EXISTS `profile` (
  `username` TEXT NOT NULL,
  `public_key` BLOB NOT NULL,
  `private_key` BLOB NOT NULL,
  `last_sync_at` TEXT NOT NULL,
  PRIMARY KEY (`username`)
);

CREATE TABLE IF NOT EXISTS `gem` (
  `id` TEXT NOT NULL,
  `name` TEXT NOT NULL,
  `desc` TEXT NOT NULL,
  `sprite` BLOB NOT NULL,
  `created_by` TEXT NOT NULL
  `created_for` TEXT NOT NULL,
  `created_at` TEXT NOT NULL,
  `obtained_at` TEXT NOT NULL,
  `is_public` BOOLEAN NOT NULL DEFAULT 0,
  `payload` BLOB NOT NULL
  PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `wanted` (
  `gem` TEXT NOT NULL,
  PRIMARY KEY (`gem`)
);

CREATE TABLE IF NOT EXISTS `trade` (
  `peername` TEXT NOT NULL,
  `unseen` BOOLEAN NOT NULL DEFAULT 0,
  `ip` TEXT NOT NULL,
  `port` INTEGER NOT NULL,
  `key` BLOB NOT NULL,
  `last_update_at` TEXT NOT NULL,
  `self_accepted` BOOLEAN NOT NULL DEFAULT 0,
  `peer_accepted` BOOLEAN NOT NULL DEFAULT 0,
  `self_fusion` BOOLEAN NOT NULL DEFAULT 0,
  `peer_fusion` BOOLEAN NOT NULL DEFAULT 0,
  PRIMARY KEY (`peername`)
);

CREATE TABLE IF NOT EXISTS `trade_state` (
  `peername` TEXT NOT NULL,
  `from_self` BOOLEAN NOT NULL,
  `offered` BOOLEAN NOT NULL,
  `gem` TEXT NOT NULL,
  PRIMARY KEY (`peername`, `from_self`, `offered`, `gem`),
  FOREIGN KEY (`peername`) REFERENCES `trade`(`peername`)
);
