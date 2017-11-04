didactic-guide (Still in search of a name)
==========================================

This is currently a work in progress. The aim is to use public domain data that noaa.gov provides
to display a running graph of solar wind.

All data is provided via noaa.gov and the ACE/SWEPAM project: https://en.wikipedia.org/wiki/Advanced_Composition_Explorer

The script utilizes the following public API: http://services.swpc.noaa.gov/products/solar-wind/

Requirements
--------------
- Python 3 and pip
- sqlite3 (if not installed already)
- (OPTIONAL) Docker - latest
- (OPTIONAL) Docker-compose - latest

Setup
------
1. `pip install -r requirements.txt`
2. `python create_db.py`

Docker Usage
--------------
- `docker-compose up -d``-d` is optional

The first time the docker container is spun up, it will call NOAA for the last week to create a bit of seed data. From there, it will call NOAA's API every minute and insert said data into the `./database/noaa.db` SQLite database. 

Additionally, the container will call NOAA's 1 -day endpoint every morning, and will call NOAA's 7-dat endpoint once per week in case there was an outage data can be recovered.

Manual Usage
--------------
This script can also be ran manually:

`python popuate.py latest|hour|day|week`

- latest: calls NOAA's plasma-5-minute endpoint
- hour: plasma-2-hour
- day: plasma-1-day
- week[default]: plasma-7-day

Running the script without specifying any command line args will automatically call the `week` arg.