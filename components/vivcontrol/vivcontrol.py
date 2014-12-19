#!/usr/bin/python

import dbhelper

config = dbhelper.loadConfig()

configId = config[0]
sensorPin1 = config[1]
sensorPin2 = config[2]
lightPin = config[3]
heatPin = config[4]
humPin = config[5]
dayTemp = config[6]
nightTemp = config[7]
minHum = config[8]
dayTimeStart = config[9]
dayTimeEnd = config[10]
interval = config[11]

print "configId=%s sensorPin1=%s  sensorPin2=%s  lightPin=%s  heatPin=%s  humPin=%s  dayTemp=%s  nightTemp=%s  minHum=%s  dayTimeStart=%s  dayTimeEnd=%s  interval=%s" % (configId,sensorPin1,sensorPin2,lightPin,heatPin,humPin,dayTemp,nightTemp,minHum,dayTimeStart,dayTimeEnd,interval)


