-- Transactions Table
CREATE TABLE "transactions" (
	'trans_id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	'user_id' INTEGER NOT NULL,
	'comp_id' INTEGER NOT NULL,
	'shares' INTEGER NOT NULL,
	'price' REAL NOT NULL,
	'time' DATETIME NOT NULL
);

-- Companies Table
CREATE TABLE 'companies' (
	'comp_id' INTEGER PRIMARY KEY AUTOINCREMENT,
	"symbol" TEXT UNIQUE NOT NULL,
	"comp_name" TEXT NOT NULL
);

-- Users Table
CREATE TABLE 'users' (
	'user_id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	'username' TEXT NOT NULL,
	'hash' TEXT NOT NULL,
	'cash' NUMERIC NOT NULL DEFAULT 10000.00
);
