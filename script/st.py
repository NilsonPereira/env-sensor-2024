#!/usr/bin/python3

import time
import numpy as np
import epics
import socket
import threading
import queue

class SENSOR:
  def __init__(self):
    self.buf = [0]
  def avg(self,V,N):
    if N<1:
      N=1
    elif N>3600:
      N=3600
    self.buf.append(V)
    self.buf = self.buf[-N:]
    return np.mean(self.buf)

# UDP server
global sock
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ("192.168.1.10", 50120)
print(f" ----\nStarting UDP server\nhost: {server_address[0]}\nport: {server_address[1]}")
sock.bind(server_address)

# create epics channels
print("Connecting epics channels ...")
#default
pvTemperature = epics.PV("NSRV:ENV:temperature")
pvRH = epics.PV("NSRV:ENV:rh")
pvPressure = epics.PV("NSRV:ENV:pressure")
pvAirQ = epics.PV("NSRV:ENV:airquality")
pvLintensity = epics.PV("NSRV:ENV:light:intensity")
pvLRed = epics.PV("NSRV:ENV:light:red")
pvLGreen = epics.PV("NSRV:ENV:light:green")
pvLBlue = epics.PV("NSRV:ENV:light:blue")
#raw
pvTemperature_RAW = epics.PV("NSRV:ENV:temperature:raw")
pvRH_RAW = epics.PV("NSRV:ENV:rh:raw")
pvPressure_RAW = epics.PV("NSRV:ENV:pressure:raw")
pvAirQ_RAW = epics.PV("NSRV:ENV:airquality:raw")
pvLintensity_RAW = epics.PV("NSRV:ENV:light:intensity:raw")
pvLRed_RAW = epics.PV("NSRV:ENV:light:red:raw")
pvLGreen_RAW = epics.PV("NSRV:ENV:light:green:raw")
pvLBlue_RAW = epics.PV("NSRV:ENV:light:blue:raw")
#offset
pvTemperature_OFF = epics.PV("NSRV:ENV:temperature:offset", auto_monitor=True)
pvRH_OFF = epics.PV("NSRV:ENV:rh:offset", auto_monitor=True)
pvPressure_OFF = epics.PV("NSRV:ENV:pressure:offset", auto_monitor=True)
pvAirQ_OFF = epics.PV("NSRV:ENV:airquality:offset", auto_monitor=True)
pvLintensity_OFF = epics.PV("NSRV:ENV:light:intensity:offset", auto_monitor=True)
pvLRed_OFF = epics.PV("NSRV:ENV:light:red:offset", auto_monitor=True)
pvLGreen_OFF = epics.PV("NSRV:ENV:light:green:offset", auto_monitor=True)
pvLBlue_OFF = epics.PV("NSRV:ENV:light:blue:offset", auto_monitor=True)
#Navg
pvTemperature_N = epics.PV("NSRV:ENV:temperature:Navg", auto_monitor=True)
pvRH_N = epics.PV("NSRV:ENV:rh:Navg", auto_monitor=True)
pvPressure_N = epics.PV("NSRV:ENV:pressure:Navg", auto_monitor=True)
pvAirQ_N = epics.PV("NSRV:ENV:airquality:Navg", auto_monitor=True)
pvLintensity_N = epics.PV("NSRV:ENV:light:intensity:Navg", auto_monitor=True)
pvLRed_N = epics.PV("NSRV:ENV:light:red:Navg", auto_monitor=True)
pvLGreen_N = epics.PV("NSRV:ENV:light:green:Navg", auto_monitor=True)
pvLBlue_N = epics.PV("NSRV:ENV:light:blue:Navg", auto_monitor=True)
#AVG
pvTemperature_AVG = epics.PV("NSRV:ENV:temperature:avg")
pvRH_AVG = epics.PV("NSRV:ENV:rh:avg")
pvPressure_AVG = epics.PV("NSRV:ENV:pressure:avg")
pvAirQ_AVG = epics.PV("NSRV:ENV:airquality:avg")
pvLintensity_AVG = epics.PV("NSRV:ENV:light:intensity:avg")
pvLRed_AVG = epics.PV("NSRV:ENV:light:red:avg")
pvLGreen_AVG = epics.PV("NSRV:ENV:light:green:avg")
pvLBlue_AVG = epics.PV("NSRV:ENV:light:blue:avg")
time.sleep(3)

# create sensors
s_Temp = SENSOR()
s_RH = SENSOR()
s_Press = SENSOR()
s_AIRQ = SENSOR()
s_LInt = SENSOR()
s_LR = SENSOR()
s_LG = SENSOR()
s_LB = SENSOR()

# global vars
global bufSensor1, bufSensor2
bufSensor1 = ""
bufSensor2 = ""
evt1 = threading.Event()
evt2 = threading.Event()

# thread workers
def datareceiver():
  print("Data receiver thread started")
  global bufSensor1, bufSensor2
  while (True):
    data, address = sock.recvfrom(128)
    if data:
      if data[0]==49:
        bufSensor1 = data
        evt1.set()
      elif data[0]==50:
        bufSensor2 = data
        evt2.set()

# launch threads
threadlist = []
t1 = threading.Thread(target=datareceiver)
threadlist.append(t1)
print("Launching thread...")
t1.start()

print("Main loop running...")
# main loop
while(True):
  evt1.clear()
  evt2.clear()
  evt1.wait()
  # receive sensor 1 data
  d1 = bufSensor1.decode('ascii').strip().split(';')
  evt2.wait()
  # receive sensor 2 data
  d2 = bufSensor2.decode('ascii').strip().split(';')
  # process data
  if len(d1)==5:
    vr = float(d1[1])
    vo = vr+pvTemperature_OFF.value
    pvTemperature_RAW.put(vr)
    pvTemperature.put(vo)
    pvTemperature_AVG.put(s_Temp.avg(vo, int(pvTemperature_N.value)))

    vr = float(d1[2])
    vo = vr+pvRH_OFF.value
    pvRH_RAW.put(vr)
    pvRH.put(vo)
    pvRH_AVG.put(s_RH.avg(vo, int(pvRH_N.value)))

    vr = float(d1[3])
    vo = vr+pvPressure_OFF.value
    pvPressure_RAW.put(vr)
    pvPressure.put(vo)
    pvPressure_AVG.put(s_Press.avg(vo, int(pvPressure_N.value)))

    vr = float(d1[4])
    vo = vr+pvAirQ_OFF.value
    pvAirQ_RAW.put(vr)
    pvAirQ.put(vo)
    pvAirQ_AVG.put(s_AIRQ.avg(vo, int(pvAirQ_N.value)))

  if len(d2)==5:
    vr = float(d2[1])
    vo = vr+pvLintensity_OFF.value
    pvLintensity_RAW.put(vr)
    pvLintensity.put(vo)
    pvLintensity_AVG.put(s_LInt.avg(vo, int(pvLintensity_N.value)))

    vr = float(d2[2])
    vo = vr+pvLRed_OFF.value
    pvLRed_RAW.put(vr)
    pvLRed.put(vo)
    pvLRed_AVG.put(s_LR.avg(vo, int(pvLRed_N.value)))

    vr = float(d2[3])
    vo = vr+pvLGreen_OFF.value
    pvLGreen_RAW.put(vr)
    pvLGreen.put(vo)
    pvLGreen_AVG.put(s_LG.avg(vo, int(pvLGreen_N.value)))

    vr = float(d2[4])
    vo = vr+pvLBlue_OFF.value
    pvLBlue_RAW.put(vr)
    pvLBlue.put(vo)
    pvLBlue_AVG.put(s_LB.avg(vo, int(pvLBlue_N.value)))

