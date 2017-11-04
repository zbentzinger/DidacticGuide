"""
TODO: implement logging module because duh.
"""

import requests
import sqlite3
import sys
#import timeit

def insertPlasmaData(json):
	"""
	Insert data into the sqlite database. Must pass a valid JSON object.
	Does not return anything.

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
	latest = 'http://services.swpc.noaa.gov/products/solar-wind/plasma-5-minute.json'
	hourly = 'http://services.swpc.noaa.gov/products/solar-wind/plasma-2-hour.json'
	daily = 'http://services.swpc.noaa.gov/products/solar-wind/plasma-1-day.json'
	weekly = 'http://services.swpc.noaa.gov/products/solar-wind/plasma-7-day.json'

	try:
		if sys.argv[1] == 'latest':
			insertPlasmaData(retrieveData(latest))
		elif sys.argv[1] == 'hour':
			insertPlasmaData(retrieveData(hourly))
		elif sys.argv[1] == 'day':
			insertPlasmaData(retrieveData(daily))
		elif sys.argv[1] == 'week':
			insertPlasmaData(retrieveData(weekly))
		else:
			sys.exit("Error: InvalidTimePeriod: ('latest','hour','day','week')")
	except IndexError:
		# Backfill for the last week. Cron will handle the minutiae
		insertPlasmaData(retrieveData(weekly))

if __name__ == '__main__':
	main()
