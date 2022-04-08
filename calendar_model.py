import datetime 

class Calendar:
    def __init__(self,raw_calendar):
        self.labels = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')
        zipped = zip(self.labels,raw_calendar)

        self.value = {k: Month(v,k) for k,v in zipped}
        
    def __getitem__(self,arg):
        #if isinstance(arg,datetime.datetime):
        ## TODO
        # if isinstance(arg,datetime.time):
        ## TODO
        if not isinstance(arg,tuple):
            month=arg
            assert month in self.labels, f"{month} is an incorrect month value"
            return self.value[month]
        elif len(arg)==2:
            day,month = arg
            return self[month][day]
        elif len(arg)==3:
            prayer,day,month = arg
            return self[day,month][prayer]
    
    def __repr__(self):
        return "\n".join(map(lambda x : x.__repr__(),self.value.values()))
    
    def dt_(self,prayer,day,month):
        h,m=self.__getitem__((prayer,day,month)).split(':')
        
    def todays_prayers(self):
        today = datetime.datetime.today()
        dow, month, dom, timme, year = today.ctime().split()
        return self[dom, month]
        
    def next_prayer(self):
        for next_label, next_prayer in self.todays_prayers().value.items():
            if not next_prayer.is_past():
                return next_label, next_prayer

    def current_prayer(self):
        next_label, next_prayer = self.next_prayer()
        
        ## TODO
        return next_prayer(self)

        
    
class Month:
    def __init__(self,calendar_month, label):
        self.label = label
        self.value = [ Day(calendar_day) for calendar_day in calendar_month.values()]
        self.length = len(self.value)
    def __repr__(self):
        return "-"*41 + f' {self.label} ' + "-"*42 + '\n' + \
               '\n'.join(map(lambda x : x.__repr__(),self.value)) + '\n' + \
                "-"*88 + '\n'
    def __getitem__(self,day):
        day_ = int(day) - 1
        assert 0 <= day_ < self.length , f"{self.label} has no {day}-th day"
        return self.value[day_]
    
   
    
    
class Day:
    def __init__(self,calendar_day):
        self.labels = ('fajr','shourouq','dhohr','asr','maghrib','icha')
        self.value = dict(zip(self.labels,map(PrayerTime,calendar_day)))

        
    def __repr__(self):  
        return " | ".join(f"{label}: {time}" for label,time in self.value.items())
    def __getitem__(self,prayer):
        assert prayer in self.labels, f"{prayer} is an incorrect prayer value"
        return self.value[prayer]

    
class PrayerTime():
    def __init__(self,calendar_prayer):
        h,m = calendar_prayer.split(':')
        self.time = datetime.time(int(h), int(m))
        
    def __repr__(self):  
        return f"{str(self.time.hour).zfill(2)}h{str(self.time.minute).zfill(2)}"
    
    def is_past(self,other_time=None):
        if other_time is None:
            return datetime.datetime.now().time() > self.time
        else: 
            return other_time > self.time
        
# cal = Calendar(parser.calendar)