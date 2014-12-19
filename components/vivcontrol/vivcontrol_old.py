#!/usr/bin/python

import time
from time import *
import sys
import RPi.GPIO as GPIO
import pigpio
import DHT22

#### <config> ####
sensorPin = 4
sensorOutsidePin = 17
lightPin = 20
heatPin = 21

dayTimeStart = 9, 00
dayTimeEnd = 21, 00
dayTemp = 26
nightTemp = 24

interval = 300

logFilePath = "data/vivcontrol.log"
#### </config> ####

ACTION_LIGHT_ON = "Light_On"
ACTION_LIGHT_OFF = "Light_Off"
ACTION_HEATING_ON = "Heating_On"
ACTION_HEATING_OFF = "Heating_Off"

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(lightPin, GPIO.OUT)
GPIO.setup(heatPin, GPIO.OUT)

PI = pigpio.pi()
PI2 = pigpio.pi()
sensor = DHT22.sensor(PI, sensorPin)
sensorOutside = DHT22.sensor(PI2, sensorOutsidePin)

logFile = open(logFilePath, "a", 0)

def isDayTime():
    now = localtime()
    tmp = now[0], now[1], now[2], dayTimeStart[0], dayTimeStart[1], 0, 0, 0, 0
    start = mktime(tmp)
    tmp = now[0], now[1], now[2], dayTimeEnd[0], dayTimeEnd[1], 0, 0, 0, 0
    end = mktime(tmp)
    now = time()
    return (now > start) and (now < end)

def light(value):
    if value and not isLightOn():
        GPIO.output(lightPin, True)
    elif not value and isLightOn():
        GPIO.output(lightPin, False)

def isLightOn():
    return GPIO.input(lightPin)

def heating(value):
    if value and not isHeatingOn():
        GPIO.output(heatPin, True)
    elif not value and isHeatingOn():
        GPIO.output(heatPin, False)

def isHeatingOn():
    return GPIO.input(heatPin)

def readTempHum():
    sensor.trigger()
    sleep(0.2)
    return sensor.temperature(), sensor.humidity()

def readTempHumOutside():
    sensorOutside.trigger()
    sleep(0.2)
    return sensorOutside.temperature(), sensorOutside.humidity()

def log(temp=None, hum=None, tempOutside=None, humOutside=None, actions=None ):
    timestamp = time()
    lightStatus = isLightOn()
    heatStatus = isHeatingOn()
    logFile.write(strftime("%Y-%m-%d %H:%M:%S", localtime(timestamp))+"\t"+str(timestamp)+"\t"+str(temp)+"\t"+str(hum)+"\t"+str(tempOutside)+"\t"+str(humOutside)+"\t"+str(lightStatus)+"\t"+str(heatStatus)+"\t"+actions+"\n")

########################

logFile.write("Time\tTimestamp\tTemperature\tHumidity\tTemperature2\tHumidity2\tLight\tHeating\tActions\n")

while True:
    tmp = readTempHum()
    tmp2 = readTempHumOutside()
    temp = tmp[0]
    hum = tmp[1]
    tempOutside = tmp2[0]
    humOutside = tmp2[1]
    day = isDayTime()
    
    actions = ""

    if day:
        if not isLightOn():
            light(True)
            actions = actions+","+ACTION_LIGHT_ON
        if (temp < dayTemp) and not isHeatingOn():
            heating(True)
            actions = actions+","+ACTION_HEATING_ON
        elif (temp > dayTemp) and isHeatingOn():
            heating(False)
            actions = actions+","+ACTION_HEATING_OFF
    else:
        if isLightOn():
            light(False)
            actions = actions+","+ACTION_LIGHT_OFF
        if (temp < nightTemp) and not isHeatingOn():
            heating(True)
            actions+","+ACTION_HEATING_ON
        elif (temp > nightTemp) and isHeatingOn():
            heating(False)
            actions = actions+","+ACTION_HEATING_OFF

    if len(actions) > 0:
        actions = actions[1:len(actions)]

    log(temp, hum, tempOutside, humOutside, actions)

    sleep(interval)

