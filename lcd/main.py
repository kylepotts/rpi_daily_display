from lcd import LCD
from ha import HA
from multiprocessing import Process,Queue,Manager
from datetime import datetime
import time
lcd = LCD()
ha = HA()


def listen_for_temp(d):
    while True:
        temp = ha.get_temp()
        temp_string = 'Temp %s F' %(temp)
        d['temp'] = temp_string.encode()
        time.sleep(10)

def listen_for_now_playing(d):
    while True:
        playing = ha.get_now_playing()
        if playing is not None:
            d['playing'] = playing.encode()
        else:
            d['playing'] = None
        time.sleep(20)

def get_time(d):
    while True:
        dt = datetime.now()
        t1 = dt.strftime("%m/%d/%Y")
        t2 = dt.strftime("%H:%M:%S")
        s = '%s\x0D%s' %(t1,t2)
        d['time'] = s.encode()
        time.sleep(5)


def write_text(d):
    while True:
        for key in d.keys():
            print(key)
            if d[key] is not None:
                s = d[key]
                s_short = (s[:30] + '..') if len(s) > 30 else s
                lcd.write(s_short.encode())
                time.sleep(10)
        time.sleep(5)

sounds = ['\xDC', '\xDD', '\xDE']
lcd.clear()
lcd.turnOnScreen()
lcd.write('\xDC')
lcd.write('Initializing...')
'''
temp = ha.get_temp()
temp_string = 'Temp %s F' %(temp)
lcd.write(temp_string.encode())
'''
manager = Manager()
d = manager.dict()

d['temp'] = None
d['playing'] = None
d['time'] = None
p1 = Process(target=listen_for_temp, args=(d,))
p2 = Process(target=listen_for_now_playing, args=(d,))
p3 = Process(target=write_text, args=(d,))
p4 = Process(target=get_time, args=(d,))
p1.start()
p2.start()
p3.start()
p4.start()


while True:
    a = 1