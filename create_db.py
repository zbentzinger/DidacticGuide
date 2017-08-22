"""
Sets up data containers for storing NOAA data.

This only needs to be ran once, prior to running the populate scripts.
"""

import sqlite3


def main():
	"""
	Creates the plasma table, takes no arguments.
	TODO: add more dbs/tables for further NOAA data collection.
	"""

	create_statement = """
		CREATE TABLE IF NOT EXISTS `PLASMA` (
		`PD_ID` INTEGER PRIMARY KEY AUTOINCREMENT,
		`TIMESTAMP` TEXT UNIQUE,
		`DENSITY` REAL,
		`SPEED` REAL,
		`TEMPERATURE` INTEGER
		);
	"""

	connection = sqlite3.connect('noaa.db')
	connection.execute(create_statement)


if __name__ == '__main__':
	main()