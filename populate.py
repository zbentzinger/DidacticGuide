"""
TODO: implement logging module because duh.
"""

import requests
import sqlite3
import sys
#import timeit

def insertPlasmaData(json):
    """
    Insert data into the `plasma` table within the sqlite database. 
    Must pass a valid JSON object. Does not return anything.

    param: json (dict) valid JSON object that consists of four keys.
    """
    insert_statement = """
        INSERT OR IGNORE INTO `PLASMA` (`TIMESTAMP`, `DENSITY`, `SPEED`, `TEMPERATURE`) 
        VALUES (?,?,?,?);
    """
    connection = sqlite3.connect('./database/noaa.db')
    try:
        with connection:
            connection.executemany(insert_statement, json)
    except sqlite3.OperationalError:
        raise

def insertMagFieldData(json):
    """
    Insert data into the `magfield` table within the sqlite database. 
    Must pass a valid JSON object. Does not return anything.

    param: json (dict) valid JSON object that consists of four keys.
    """
    insert_statement = """
        INSERT OR IGNORE INTO `MAGFIELD` (`TIMESTAMP`, `BX`, `BY`, `BZ`, `PHI`, `THETA`, `BT`) 
        VALUES (?,?,?,?,?,?,?);
    """
    connection = sqlite3.connect('./database/noaa.db')
    try:
        with connection:
            connection.executemany(insert_statement, json)
    except sqlite3.OperationalError:
        raise

def retrieveData(url):
    """
    TODO: create method to standardize data.
    Gets plasma speed and density from NOAA.gov that can be stored.

    param: url (string) valid http URL to noaa.gov
    return: data (dict) formatted JSON
    """
    request = requests.get(url)
    data = request.json()
    data.pop(0) #Don't need NOAAs schema definition.
    return data

def main():
    """Run the program"""
    latestPlasma = 'http://services.swpc.noaa.gov/products/solar-wind/plasma-5-minute.json'
    hourlyPlasma = 'http://services.swpc.noaa.gov/products/solar-wind/plasma-2-hour.json'
    dailyPlasma = 'http://services.swpc.noaa.gov/products/solar-wind/plasma-1-day.json'
    weeklyPlasma = 'http://services.swpc.noaa.gov/products/solar-wind/plasma-7-day.json'

    latestMag = 'http://services.swpc.noaa.gov/products/solar-wind/mag-5-minute.json'
    hourlyMag = 'http://services.swpc.noaa.gov/products/solar-wind/mag-2-hour.json'
    dailyMag = 'http://services.swpc.noaa.gov/products/solar-wind/mag-1-day.json'
    weeklyMag = 'http://services.swpc.noaa.gov/products/solar-wind/mag-7-day.json'

    try:
        if sys.argv[1] == 'latest':
            insertPlasmaData(retrieveData(latestPlasma))
            insertMagFieldData(retrieveData(latestMag))
        elif sys.argv[1] == 'hour':
            insertPlasmaData(retrieveData(hourlyPlasma))
            insertMagFieldData(retrieveData(hourlyMag))
        elif sys.argv[1] == 'day':
            insertPlasmaData(retrieveData(dailyPlasma))
            insertMagFieldData(retrieveData(dailyMag))
        elif sys.argv[1] == 'week':
            insertPlasmaData(retrieveData(weeklyPlasma))
            insertMagFieldData(retrieveData(weeklyMag))
        else:
            sys.exit("Error: InvalidTimePeriod: ('latest','hour','day','week')")
    except IndexError:
        # Backfill for the last week. Cron will handle the minutiae
        insertPlasmaData(retrieveData(weeklyPlasma))
        insertMagFieldData(retrieveData(weeklyMag))

if __name__ == '__main__':
    main()
