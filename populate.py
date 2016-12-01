import requests
import sqlite3
import sys
#import timeit


def createDB():
	"""Creates a sqlite database"""
	open('data.db', 'a').close()
	create_statement = """
		CREATE TABLE 'plasma' (
		`timestamp` TEXT UNIQUE,
		`density` REAL,
		`speed` REAL,
		`temperature`INTEGER
		);
	"""
	connection = sqlite3.connect('data.db')
	try:
		with connection:
			connection.execute(create_statement)
	except sqlite3.OperationalError:
		# Database has already been setup
		pass

def insertData(json):
	"""Insert data into the sqlite database. Must pass a valid JSON object"""
	insert_statement = """
		INSERT OR IGNORE INTO `plasma` (`timestamp`, `density`, `speed`, `temperature`) 
		VALUES (?,?,?,?);
	"""
	connection = sqlite3.connect('data.db')
	try:
		with connection:
			connection.executemany(insert_statement, json)
	except sqlite3.OperationalError:
		raise

def retrieveData(url):
	"""GET the JSON from noaa.gov and format it"""
	request = requests.get(url)
	data = request.json()
	data.pop(0)
	return data

def main():
	"""Run the program"""
	latest = 'http://services.swpc.noaa.gov/products/solar-wind/plasma-5-minute.json'
	hourly = 'http://services.swpc.noaa.gov/products/solar-wind/plasma-2-hour.json'
	daily = 'http://services.swpc.noaa.gov/products/solar-wind/plasma-1-day.json'
	weekly = 'http://services.swpc.noaa.gov/products/solar-wind/plasma-7-day.json'

	try:
		if sys.argv[1] == 'latest':
			insertData(retrieveData(latest))
		elif sys.argv[1] == 'hour':
			insertData(retrieveData(hourly))
		elif sys.argv[1] == 'day':
			insertData(retrieveData(daily))
		elif sys.argv[1] == 'week':
			insertData(retrieveData(weekly))
		else:
			sys.exit("Error: InvalidTimePeriod: ('latest','hour','day','week')")
	except IndexError:
		# Create the database, and backfill for the last week. Cron will handle the minutiae
		createDB()
		insertData(retrieveData(weekly))

if __name__ == '__main__':
	main()
