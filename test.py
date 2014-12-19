#!/usr/bin/python

import psycopg2
import sys

configId = None
sensorPin1 = None
sensorPin2 = None
lightPin = None
heatPin = None
humPin = None
dayTimeStart = None
dayTimeEnd = None
dayTemp = None
nightTemp = None
interval = None

selectConfig = "SELECT id,sensorpin1,sensorpin2,lightpin,heatpin,humpin,daytemp,nighttemp,minhum,daystart,dayend,checkinterval FROM config WHERE active=TRUE;"

def loadConfig():

	con = None

	try:

		global configId,sensorPin1,sensorPin2,lightPin,heatPin,humPin,dayTimeStart,dayTimeEnd,dayTemp,nightTemp,interval 
		 
		con = psycopg2.connect("host=localhost dbname=vivcontrol user=postgres") 
		cur = con.cursor()
		cur.execute(selectConfig)
		result = cur.fetchone()
		return result;

	except psycopg2.DatabaseError, e:
		print 'Error %s' % e
		return None
   
	finally:

		if con:
			con.close()


loadConfig()