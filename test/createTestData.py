#!/usr/bin/python

import sys
sys.path.append( "../components/vivcontrol" )
from dbhelper import DBHelper
import datetime
import time

db = DBHelper()

config = db.loadConfig()

if config is None:
	values = "test","4","17","20","21","22","26","24","60","2","2","2","32400","75600","300", "True"
	db.addConfig(values)
	config = db.loadConfig()

today = datetime.datetime.now()
oneHour = datetime.timedelta(hours=1)
sevenHoursAgo = today - datetime.timedelta(hours=7);

temp1 = 20
temp2 = 21
hum1 = 50
hum2 = 51
heat = False
light = False
hum = False

for x in range(0, 7):
	curTime = time.mktime(sevenHoursAgo.timetuple())
	# logtime,config,heating,light,hum,temp1,temp2,hum1,hum2
	toInsert = curTime, config[0], heat, light, hum, temp1, temp2, hum1, hum2
	db.addLog(toInsert)
	sevenHoursAgo += oneHour
	temp1 += 1;
	temp2 += 1;
	hum1 += 1;
	hum2 += 1;
	heat = not heat;
	light = not light;
	hum = not hum;

db.close()
	