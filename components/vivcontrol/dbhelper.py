#!/usr/bin/python

import psycopg2
import sys
import time

selectConfigStmt = "SELECT id,sensorpin1,sensorpin2,lightpin,heatpin,humpin,daytemp,nighttemp,minhum,lightcontrol,heatcontrol,humcontrol,daystart,dayend,checkinterval FROM config WHERE active=TRUE;"
addConfigStmt = "INSERT INTO config (name,sensorpin1,sensorpin2,lightpin,heatpin,humpin,daytemp,nighttemp,minhum,lightcontrol,heatcontrol,humcontrol,daystart,dayend,checkinterval,active) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
addLogStmt = "INSERT INTO log(logtime,config,heating,light,hum,temp1,temp2,hum1,hum2) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
getLogStmt = "SELECT logtime,config,heating,light,hum,temp1,temp2,hum1,hum2 FROM log WHERE logtime>%s AND logtime<%s;"

class DBHelper:

	def __init__(self, host="localhost", dbname="vivcontrol", dbuser="postgres"):
		try:
			self.con = psycopg2.connect("host="+host+" dbname="+dbname+" user="+dbuser) 

		except psycopg2.DatabaseError, e:
			print 'Could not connect to database! %s' % e


	def loadConfig(self):
		try:
			cur = self.con.cursor()
			cur.execute(selectConfigStmt)
			result = cur.fetchone()
			return result

		except psycopg2.DatabaseError, e:
			print 'Could not load config %s' % e
			return None

	def addConfig(self, values):
		try:
			cur = self.con.cursor()
			cur.execute(addConfigStmt,values)
			self.con.commit()

		except psycopg2.DatabaseError, e:
			print 'Could not add config %s' % e
			return None

	def addLog(self, values):
		try:
			cur = self.con.cursor()
			cur.execute(addLogStmt,values)
			self.con.commit()

		except psycopg2.DatabaseError, e:
			print 'Could not add log %s' % e
			return None
	   

	def getLog(self, fromTime, toTime):
		fromInSec = 0;
		toInSec = time.time();
		if fromTime is not None:
			fromInSec = time.strptime(fromTime, "%Y-%m-%dT%H:%M:%S").time()
		if toTime is not None:
			toInSec = time.strptime(toTime, "%Y-%m-%dT%H:%M:%S").time()

		try:
			cur = self.con.cursor()
			cur.execute(getLogStmt, fromInSec, toInSec)
			result = cur.fetchall()
			return result

		except psycopg2.DatabaseError, e:
			print 'Could not get logs %s' % e
			return None


	def close(self):
		if self.con:
			self.con.close()
