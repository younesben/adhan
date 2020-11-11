#!/usr/bin/env python

import datetime
import time
import sys

from calendarrr import Calendar
import json

with open('/home/pi/adhan/calendar.json','r') as f:
    cal = json.load(f)
calendar = Calendar(cal)


from crontab import CronTab
system_cron = CronTab(user='pi')

now = datetime.datetime.now()

generic_command = '''
/bin/bash /home/pi/adhan/run_live.sh && \
sleep 600 && \
/usr/bin/docker rm -f live \
> /dev/null 2>&1 '''


strPlayFajrAzaanMP3Command = generic_command
strPlayAzaanMP3Command =  generic_command
strUpdateCommand = '/home/pi/adhan/venv/bin/python /home/pi/adhan/updateAzaanTimers.py >> /home/pi/adhan/adhan.log 2>&1'
strClearLogsCommand = 'truncate -s 0 /home/pi/adhan/adhan.log 2>&1'
strJobComment = 'rpiAdhanClockJob'




#HELPER FUNCTIONS
#---------------------------------
#---------------------------------
#Function to add azaan time to cron




def addAzaanTime (strPrayerName, prayer, objCronTab):
  if strPrayerName == 'fajr':
    strCommand = strPlayFajrAzaanMP3Command
  else:
    strCommand = strPlayAzaanMP3Command
  job = objCronTab.new(command=strCommand,comment=strPrayerName)
  hour, minute = prayer.time.hour, prayer.time.minute
  job.minute.on(minute)
  job.hour.on(hour)
  job.set_comment(strJobComment)
  print(job)
  return

def addDarkiceRestart (strPrayerName, prayer, objCronTab):

  job = objCronTab.new(command="docker restart darkice",comment="restarting streaming")
  restart_time = (datetime.datetime.combine(datetime.date(1, 1, 1), prayer.time) - datetime.timedelta(minutes=15)).time()
  hour, minute = restart_time.hour, restart_time.minute
  job.minute.on(minute)
  job.hour.on(hour)
  job.set_comment(strJobComment)
  print(job)
  return

def addUpdateCronJob (objCronTab, strCommand):
  job = objCronTab.new(command=strCommand)
  job.minute.on(15)
  job.hour.on(3)
  job.set_comment(strJobComment)
  print(job)
  return

def addClearLogsCronJob (objCronTab, strCommand):
  job = objCronTab.new(command=strCommand)
  job.day.on(1)
  job.minute.on(0)
  job.hour.on(0)
  job.set_comment(strJobComment)
  print(job)
  return
#---------------------------------
#---------------------------------
#HELPER FUNCTIONS END

# Remove existing jobs created by this script
system_cron.remove_all(comment=strJobComment)

today_prayers=calendar.todays_prayers()
print(today_prayers)
for label,prayer in today_prayers.value.items(): 
  if label != "shourouq":
    # addDarkiceRestart(label, prayer, system_cron)
    addAzaanTime(label, prayer, system_cron)
    

# Run this script again overnight
addUpdateCronJob(system_cron, strUpdateCommand)

# Clear the logs every month
addClearLogsCronJob(system_cron,strClearLogsCommand)

system_cron.write_to_user(user='pi')
print('Script execution finished at: ' + str(now))