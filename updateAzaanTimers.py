#!/usr/bin/env python

from dotenv import load_dotenv
load_dotenv()
from crontab import CronTab
import sys
import os
import datetime
import time
from calendar_model import Calendar
import json


HOME = os.environ.get('HOME')


ADHAN_FILE = os.environ.get("ADHAN_FILE")
MPLAYER = os.environ.get("MPLAYER")
KARADIO_URL = os.environ.get("KARADIO_URL")
LOGGING = bool(int(os.environ.get("LOGGING")))
BROADCASTING = bool(int(os.environ.get("BROADCASTING")))
SLEEP_TIME = float(os.environ.get("SLEEP_TIME"))


RADIO_URL = os.environ.get("RADIO_URL")
RADIO_PORT = os.environ.get("RADIO_PORT")
MODE = os.environ.get("MODE")
MOSQUEE = os.environ.get("MOSQUEE")


ADHAN_HOME = f"{HOME}/adhan"
PYTHON = f"{ADHAN_HOME}/venv/bin/python"
PUBLISH_CMD = f'{PYTHON} {ADHAN_HOME}/broker/mqtt/sender.py'
MOUNT_POINT = f"{MOSQUEE}_{MODE}"

##############################################################################

REPORT_BEGIN_BROKER_CMD = f'msg="Beginning of broadcast : `date`" && {PUBLISH_CMD} {MOSQUEE}/info $msg' if LOGGING else ""
LAUNCH_BROADCAST_CMD = f"/bin/bash {ADHAN_HOME}/run_{MODE}.sh" if BROADCASTING else ""
LAUNCH_RADIO_CMD = f"{PUBLISH_CMD} {MOSQUEE}/start http://{RADIO_URL}:{RADIO_PORT}/{MOUNT_POINT}.mp3"
PLAY_ADHAN_CMD = f"{MPLAYER} {ADHAN_HOME}/{ADHAN_FILE}" if all(
    (MPLAYER, ADHAN_FILE)) else ""
STOP_BROADCAST_CMD = ""
STOP_RADIO_CMD = f"{PUBLISH_CMD} {MOSQUEE}/stop"
REPORT_END_BROKER_CMD = f'msg="End of broadcast : `date`" && {PUBLISH_CMD} {MOSQUEE}/info $msg' if LOGGING else ""
SLEEP_CMD = f"/bin/sleep {SLEEP_TIME} " if SLEEP_TIME and SLEEP_TIME > 0 else ""

##############################################################################

with open(f'{ADHAN_HOME}/calendar.json', 'r') as f:
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

heartbeat_command = f'msg="Raspberry heart beat : `date`" && {PUBLISH_CMD} {MOSQUEE}/info $msg' if LOGGING else ""

strPlayFajrAzaanMP3Command = generic_command
strPlayAzaanMP3Command = generic_command
strUpdateCommand = f'{PYTHON} {ADHAN_HOME}/updateAzaanTimers.py >> {ADHAN_HOME}/adhan.log 2>&1'
strClearLogsCommand = f'truncate -s 0 {ADHAN_HOME}/adhan.log 2>&1'
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
