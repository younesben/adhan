#!/usr/bin/env python

from crontab import CronTab
import sys
import os
import datetime
import time
from calendarrr import Calendar
import json


ADHAN_FILE = ""
MPLAYER = ""
KARADIO_URL = ""
LOGGING = True
BROADCASTING = True
SLEEP_TIME = 600


RADIO_URL = "radio.mysjid.com"
RADIO_PORT = "8000"
MODE = "live"
MOSQUEE = "rosny"


PWD = os.getcwd()
PYTHON = f"{PWD}/venv/bin/python"
LOGGING_CMD = f' `date`" && {PYTHON} {PWD}/broker/topics/sender.py "{MOSQUEE}.info" $msg'

##############################################################################

REPORT_BEGIN_BROKER_CMD = f'msg="Beginning of broadcast :{LOGGING_CMD}' if LOGGING else ""
LAUNCH_BROADCAST_CMD = f"/bin/bash {PWD}/run_{MODE}.sh" if BROADCASTING else ""
LAUNCH_RADIO_CMD = f"/usr/bin/curl http://{KARADIO_URL}/?instant='http://{RADIO_URL}:{RADIO_PORT}/{MODE}-{MOSQUEE}.mp3'" if KARADIO_URL else ""
PLAY_ADHAN_CMD = f"{MPLAYER} {PWD}/{ADHAN_FILE}" if all(
    (MPLAYER, ADHAN_FILE)) else ""
STOP_BROADCAST_CMD = f"/usr/bin/docker rm -f {MODE}" if BROADCASTING else ""
STOP_RADIO_CMD = f"/usr/bin/curl http://{KARADIO_URL}/?stop" if KARADIO_URL else ""
REPORT_END_BROKER_CMD = f'msg="End of broadcast :{LOGGING_CMD}' if LOGGING else ""
SLEEP_CMD = f"/bin/sleep {SLEEP_TIME/2} " if SLEEP_TIME and SLEEP_TIME > 0 else ""

##############################################################################

with open(f'{PWD}/calendar.json', 'r') as f:
    cal = json.load(f)
    calendar = Calendar(cal)


system_cron = CronTab(user='pi')

now = datetime.datetime.now()

commands = [
    REPORT_BEGIN_BROKER_CMD,
    LAUNCH_BROADCAST_CMD,
    LAUNCH_RADIO_CMD,
    SLEEP_CMD,
    PLAY_ADHAN_CMD,
    SLEEP_CMD,
    STOP_BROADCAST_CMD,
    STOP_RADIO_CMD,
    REPORT_END_BROKER_CMD
]

generic_command = (' && ').join(
    i for i in commands if i) + f" > /dev/null 2>&1 "

heartbeat_command = f'msg="Raspberry heart beat :{LOGGING_CMD}' if LOGGING else ""

strPlayFajrAzaanMP3Command = generic_command
strPlayAzaanMP3Command = generic_command
strUpdateCommand = f'{PYTHON} {PWD}/updateAzaanTimers.py >> {PWD}/adhan.log 2>&1'
strClearLogsCommand = f'truncate -s 0 {PWD}/adhan.log 2>&1'
strJobComment = 'rpiAdhanClockJob'


#HELPER FUNCTIONS
#---------------------------------
#---------------------------------
#Function to add azaan time to cron


def addHeartBeatCronJob(objCronTab, strCommand, interval=15):
  job = objCronTab.new(command=strCommand)
  job.minute.every(interval)
  job.set_comment(strJobComment)
  print(job, '\n', '-'*40)
  return


def addAzaanTime(strPrayerName, prayer, objCronTab):
  if strPrayerName == 'fajr':
    strCommand = strPlayFajrAzaanMP3Command
  else:
    strCommand = strPlayAzaanMP3Command
  job = objCronTab.new(command=strCommand, comment=strPrayerName)
  hour, minute = prayer.time.hour, prayer.time.minute
  job.minute.on(minute)
  job.hour.on(hour)
  job.set_comment(strJobComment)
  print(job, '\n', '-'*40)
  return


def addUpdateCronJob(objCronTab, strCommand):
  job = objCronTab.new(command=strCommand)
  job.minute.on(15)
  job.hour.on(3)
  job.set_comment(strJobComment)
  print(job, '\n', '-'*40)
  return


def addClearLogsCronJob(objCronTab, strCommand):
  job = objCronTab.new(command=strCommand)
  job.day.on(1)
  job.minute.on(0)
  job.hour.on(0)
  job.set_comment(strJobComment)
  print(job, '\n', '-'*40)
  return
#---------------------------------
#---------------------------------
#HELPER FUNCTIONS END


# Remove existing jobs created by this script
system_cron.remove_all(comment=strJobComment)

today_prayers = calendar.todays_prayers()
print(today_prayers)
for label, prayer in today_prayers.value.items():
  if label != "shourouq":
    # addDarkiceRestart(label, prayer, system_cron)
    addAzaanTime(label, prayer, system_cron)

# Hearbeat job
if LOGGING:
  addHeartBeatCronJob(system_cron, heartbeat_command)

# Run this script again overnight
addUpdateCronJob(system_cron, strUpdateCommand)

# Clear the logs every month
addClearLogsCronJob(system_cron, strClearLogsCommand)

system_cron.write_to_user(user='pi')
print('Script execution finished at: ' + str(now))
