#rdb-fullstack


This repo is for my submission to Udacity nanodegree - Fullstack Developer.

Currently at Project 3


#tournament

## Steps to setup
Please install the python postgressql library (e.g. pip install Psycopg2)

1. At the project directory, enter Postgres Command Line (e.g. psql)
2. install database and views by \i tournament.sql
3. Exit Psql by \q
4. Run tournament test by python tournament_test.py
5. All pass!

# Catalog

##Setup

###Update settings at application.py:
- Change the Client ID and Client Secret
- Change the secret key of the app
- Change the callback url

###Setup database

```bash
python addData.py
```

##Run project
```bash
python application.py
```
