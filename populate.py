import requests
import sqlite3
import sys


def createDB():
	"""Creates a sqlite database to store solar wind data in"""
	open('data.db', 'a').close()
	query = """
		CREATE TABLE 'plasma' (
		`timestamp` TEXT UNIQUE,
		`density` REAL,
		`speed` REAL,
		`temperature`INTEGER
		);
	"""
	executeQuery(query)

def executeQuery(query):
	"""Executes SQL queries and returns an output array for SELECT statements"""
	output = []
	try:
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()
		cursor.execute(query)
		output = cursor.fetchall()
		connection.commit()
		connection.close()
	except sqlite3.IntegrityError:
		# Just a duplicate timestamp, no need to crash the program
		pass
	finally:
		return output

def insertData(json):
	"""Insert data into the sqlite database. Must pass a valid JSON object"""
	for row in json:
		date = '"{}"'.format(row[0])
		density = row[1]
		speed = row[2]
		temp = row[3]
		insert_statement = """
			INSERT INTO `plasma` (`timestamp`, `density`, `speed`, `temperature`) 
			VALUES ({}, {}, {}, {});
		""".format(date, density, speed, temp)
		executeQuery(insert_statement)

def getNewestEntry():
	"""return the newest entry in the database based on timestamp"""
	query = 'select timestamp from plasma order by timestamp desc limit 1;'
	return executeQuery(query)[0][0]


def retrieveData(url):
	"""GET the JSON from noaa.gov and format it"""
	request = requests.get(url)
	data = request.json()
	data.pop(0)
	return data

def main():
	"""Run the program"""
	latest = 'http://services.swpc.noaa.gov/products/solar-wind/plasma-5-minute.json'
	archive = 'http://services.swpc.noaa.gov/products/solar-wind/plasma-7-day.json'
	try:
		if sys.argv[1] == 'latest':
			insertData(retrieveData(latest))
		elif sys.argv[1] == 'backfill':
			insertData((retrieveData(archive)))
	except IndexError:
		createDB()
		insertData(retrieveData(archive))

if __name__ == '__main__':
	main()
