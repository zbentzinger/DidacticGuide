"""
Sets up data containers for storing NOAA data.

This only needs to be ran once, prior to running the populate scripts.
"""

import os
import sqlite3


def main():
    """
    Creates the plasma and magnetic field tables, takes no arguments.
    TODO: add more dbs/tables for further NOAA data collection.
    """

    plasma = """
        CREATE TABLE IF NOT EXISTS `PLASMA` (
        `PD_ID` INTEGER PRIMARY KEY AUTOINCREMENT,
        `TIMESTAMP` TEXT UNIQUE,
        `DENSITY` REAL,
        `SPEED` REAL,
        `TEMPERATURE` INTEGER
        );
    """
    magField = """
        CREATE TABLE IF NOT EXISTS `MAGFIELD` (
        `MAG_ID` INTEGER PRIMARY KEY AUTOINCREMENT,
        `TIMESTAMP` TEXT UNIQUE,
        `BT` REAL,
        `BX` REAL,
        `BY` REAL,
        `BZ` REAL,
        `THETA` REAL,
        `PHI` REAL
        );
    """

    dbPath = "./database/noaa.db"
    os.makedirs(os.path.dirname(dbPath), exist_ok=True)

    connection = sqlite3.connect(dbPath)
    connection.execute(plasma)
    connection.execute(magField)


if __name__ == '__main__':
    main()