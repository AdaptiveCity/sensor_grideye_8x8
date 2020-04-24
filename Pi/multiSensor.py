#! /usr/bin/python3

# for dev / debug
DEBUG_LOG = False

import time
import board
import busio

import simplejson as json
import requests

import RPi.GPIO as GPIO
import time
import random
import board
import busio
import adafruit_amg88xx
import adafruit_dotstar as dotstar
import math
import numpy as np
from numpy import interp



i2c = busio.I2C(board.SCL, board.SDA)
amg = adafruit_amg88xx.AMG88XX(i2c)#had to modify smbus.py

 
# On-board DotStar for boards including Gemma, Trinket, and ItsyBitsy
dots = dotstar.DotStar(board.SCK, board.MOSI, 64, brightness=0.1)
# MAIN LOOP

import sys

from time_buffer import TimeBuffer

# info sent in json packet to feed handler
SENSOR_ID = '8x8_IR'
SENSOR_TYPE = 'grideye'
ACP_TOKEN = 'testtoken'

# Declare globals
i2c=None
amg=None
dots=None

EVENT_S="START"
EVENT_F="FINISH"
MIN_TEMP=16
MAX_TEMP=30

color_pallete=[
[ 32 , 17 , 89 ],
[ 27 , 17 , 89 ],
[ 22 , 17 , 90 ],
[ 17 , 16 , 90 ],
[ 16 , 21 , 90 ],
[ 16 , 25 , 90 ],
[ 16 , 30 , 90 ],
[ 16 , 35 , 90 ],
[ 15 , 40 , 90 ],
[ 15 , 45 , 91 ],
[ 15 , 49 , 91 ],
[ 14 , 54 , 91 ],
[ 14 , 60 , 91 ],
[ 14 , 65 , 91 ],
[ 14 , 70 , 92 ],
[ 13 , 75 , 92 ],
[ 13 , 80 , 92 ],
[ 13 , 85 , 92 ],
[ 12 , 90 , 92 ],
[ 12 , 92 , 89 ],
[ 12 , 92 , 83 ],
[ 12 , 93 , 78 ],
[ 12 , 93 , 73 ],
[ 11 , 93 , 68 ],
[ 11 , 93 , 62 ],
[ 11 , 93 , 57 ],
[ 10 , 94 , 52 ],
[ 10 , 94 , 46 ],
[ 10 , 94 , 40 ],
[ 10 , 94 , 35 ],
[ 9 , 94 , 29 ],
[ 9 , 94 , 23 ],
[ 9 , 94 , 18 ],
[ 9 , 94 , 12 ],
[ 11 , 95 , 8 ],
[ 16 , 95 , 8 ],
[ 22 , 95 , 8 ],
[ 27 , 95 , 7 ],
[ 33 , 95 , 7 ],
[ 39 , 96 , 7 ],
[ 45 , 96 , 7 ],
[ 50 , 96 , 6 ],
[ 56 , 96 , 6 ],
[ 62 , 96 , 6 ],
[ 68 , 96 , 5 ],
[ 74 , 96 , 5 ],
[ 80 , 97 , 5 ],
[ 86 , 97 , 5 ],
[ 92 , 97 , 4 ],
[ 97 , 96 , 4 ],
[ 97 , 90 , 4 ],
[ 98 , 84 , 3 ],
[ 98 , 78 , 3 ],
[ 98 , 71 , 3 ],
[ 98 , 65 , 3 ],
[ 98 , 59 , 2 ],
[ 98 , 52 , 2 ],
[ 98 , 46 , 1 ],
[ 99 , 40 , 1 ],
[ 99 , 33 , 1 ],
[ 99 , 27 , 1 ],
[ 99 , 20 , 0 ],
[ 99 , 13 , 0 ],
[ 100 , 6 , 0 ]]

class Sensor(object):
        def __init__(self):
               global i2c
               global amg
               global dots
              
               self.SAMPLE_HISTORY_SIZE = 100000
               self.SAMPLE_EVENT_SIZE = 30
               
               self.sample_history_index = 0
               self.sample_history = [None]*self.SAMPLE_HISTORY_SIZE

               #DON'T FORGET TO ADD SETTIGNS
               self.sample_buffer = TimeBuffer(size=self.SAMPLE_HISTORY_SIZE, settings={"LOG_LEVEL":0})
               self.raw_buffer = TimeBuffer(size=self.SAMPLE_HISTORY_SIZE, settings={"LOG_LEVEL":0})
               
               self.event_buffer = TimeBuffer(size=self.SAMPLE_EVENT_SIZE, settings=None)

               self.event_buffer.put(time.time(),"Begin")
               
               self.last_save=time.time()
               self.prev_send_time=None

               amg=self.init_grideye()
               dots=self.init_dotstar()
                 
               
               self.prev=None
               #load config here if have it
               
               self.last_event=None
               self.last_sent=None
               self.mid_event=False;

               self.event_start=None
               self.event_finish=None
               
        def init_dotstar(self):
               global dots
                # On-board DotStar for boards including Gemma, Trinket, and ItsyBitsy
               dots = dotstar.DotStar(board.SCK, board.MOSI, 64, brightness=0.25)
               return dots

        def init_grideye(self):
               global amg
                             
               # Create the I2C bus
               i2c = busio.I2C(board.SCL, board.SDA)
               amg = adafruit_amg88xx.AMG88XX(i2c)#had to modify smbus.py
                     
               return amg

               
               
        def send_data(self,post_data, token):
               response = requests.post('http://128.232.65.223:80/test/feedmaker/test.feed/general',
                                headers={'X-Auth-Token': token },
                                json=post_data
                                )
               print("status code",response.status_code)
        def update_LED(self, pixels):
            i=0
            for pixel in pixels:       
                remap=interp(pixel,[MIN_TEMP,MAX_TEMP],[0,63]).astype(np.int)      
                colors=color_pallete[remap]
                dots[i] = (colors[0], colors[1], colors[2])
                i+=1
        def get_value(self):
            global amg
            #time.sleep(0.1)
            return np.array(amg.pixels).flatten()


        def latest_buffer_val(self):
            sample_value, offset = self.sample_buffer.median(0,1)
             #get median weight for 1s
            latest_sample=self.sample_buffer.get(0)["value"]
            #print(sample_value, latest_sample)
            if (not sample_value== None) and (not latest_sample==None):
                 if(sample_value>latest_sample):
                    return  sample_value
                 else:
                    return latest_sample
            else:
                return None

             
        #true if median for 1s is more than 16 or mic==1
        #Returns tuple <Test true/false>, <next offset>
        def test_walk_avg(self,offset,duration):
            m,next_offset=self.sample_buffer.mean(offset,duration)
            
            if not m==None:
                return m
            else:
                return None #none none

        def test_walk_med(self,offset,duration):
                    m,next_offset=self.sample_buffer.median(offset,duration)
                    
                    if not m==None:
                        return m
                    else:
                        return None #none none
                
        def test_event_new(self,offset, duration):
            walked, offset=self.test_walk(offset, duration)
            #deleted additinal if statement from sensor.y
            if walked:
                return walked
            else:
                return None

            
        def test_event(self, ts):
            event_S=self.test_walk_med(0,0.5)#0.5
            event_F=self.test_walk_med(0,2)#2
           # ts=time.time()

           # print("S,F: ", event_S,event_F)    

            #Catch beginning of event
            if not event_S is None:
               # print("event delta ", event_S-16)
                
                if (event_S>0.3 and self.event_buffer.get(0)["value"]!=EVENT_S):#event_S>40
                    print("NEW Started")
                    self.event_start=ts
                    self.event_buffer.put(ts,EVENT_S)
                    self.send_event(ts,EVENT_S,0,0,0,0)
                    #send_event(self,ts,sensor_reading,dur, med,mean):
                    
            if not event_F is None and not event_S is None:
            
                if(self.event_buffer.get(0)["value"]!=EVENT_F and self.event_buffer.get(0)["value"]!="Begin"):
                    if (event_F<0.3 and event_S<0.4) :#if (event_F<10 and event_S is None)
                    
                        self.event_finished=ts
                        print("NEW Finished")
                        dur=  self.event_finished- self.event_start
                        
                        med=99#med,a=self.raw_buffer.median(0,dur+0.5)
                        mean=99#self.raw_buffer.average(0,dur+0.5)
                        max_val=99#self.raw_buffer.maximum(0,dur+0.5)
                        if(max_val<16):
                            max_val=16
                        self.event_buffer.put(ts,EVENT_F)
                        self.send_event(ts,EVENT_F,dur, med, mean,max_val)

                        #self.print_buffer()                        
                        
                        
#                   self.mid_event=False      
          
            #return event

        def print_buffer(self):
            for i in range(self.SAMPLE_EVENT_SIZE):
                if not self.event_buffer.get(i) is None:
                    print(self.event_buffer.get(i))
        
        def moving_average(self, value,perc,cutoff):
            if self.prev==None:
                self.prev=value
            value=self.prev*(1-perc)+value*(perc)#self.prev*(perc)+value*(1-perc)
            #print(value, self.prev)
            self.prev=value
            
            if(value<cutoff):
                value =0
            return value
            
        def normalize_sample(self, value):
            print(value)
            #value=value -16
            if(value<MIN_TEMP):
                return 0
            elif(value>MAX_TEMP):
                return 1
            else:
                 return (value-MIN_TEMP)/(MAX_TEMP-MIN_TEMP)
    
        def process_sample(self, ts,value):
           
            t_start= time.process_time()
            
            #store reading and timestamp in the buffer
            value=self.normalize_sample(value)
            print(value)
            #raw value
            self.raw_buffer.put(ts,value)
            
            value=self.moving_average(value, 0.05,0.15)#0.05,20
            #print(og,value)
            self.sample_buffer.put(ts,value)

            #update the screen
            #self.update_lcd(ts)

            #send event to platform
            self.test_event(ts)

            if self.prev_send_time is None:
                self.prev_send_time=ts
                
            if ts-self.prev_send_time>300:
                #sample_value, offset = self.sample_buffer.median(0,2) # from latest ts, back 2s
                self.send_watchdog(ts)
                

        #save to buffer csv file
        def save_buffer(ts):
            if (ts-self.last_save)>60:
                self.sample_buffer.save("Wednesday_morning.csv")
                self.last_save=time.time()
                print("SAVED")

        
        def send_event(self,ts,sensor_reading,dur, med,mean,max_val):
               
               print ("SENDING DATA {}, {}".format(sensor_reading, time.ctime(ts)))
               post_data = { 'request_data': [ { 'acp_id': SENSOR_ID,
                                                     'acp_type': SENSOR_TYPE,
                                                     'acp_ts': ts,
                                                     'intensity': sensor_reading,
                                                     'duration': dur,
                                                     'median': med,
                                                     'mean': mean,
                                                     'max':max_val,
                                                     'watchdog':0,
                                                     'acp_units': 'vibration_level',
                                                     'mic_reading':0
                                                                      }
                                                                    ]
                                            }
               #self.send_data(post_data, ACP_TOKEN)
               self.prev_send_time = ts              
              # time.sleep(0.1)
               
               if DEBUG_LOG:
                      print("loop send data at {:.3f} secs.".format(time.process_time() - t_start))

        def send_watchdog(self,ts):
                       
                       print ("SENDING DATA {}, {}".format('WATCHDOG', time.ctime(ts)))
                       post_data = { 'request_data': [ { 'acp_id': SENSOR_ID,
                                                             'acp_type': SENSOR_TYPE,
                                                             'acp_ts': ts,
                                                             'intensity': 0,
                                                             'duration': 0,
                                                             'median': 0,
                                                             'mean': 0,
                                                             'max':0,
                                                             'watchdog':1,
                                                             'acp_units': 'vibration_level',
                                                             'mic_reading':0
                                                                              }
                                                                            ]
                                                    }
                       self.send_data(post_data, ACP_TOKEN)
                       self.prev_send_time = ts              
                      # time.sleep(0.1)
                       
                       if DEBUG_LOG:
                              print("loop send data at {:.3f} secs.".format(time.process_time() - t_start))
                      
               
        def finish(self):
            print("\n"+"GPIO cleanup()...")
            GPIO.cleanup()
            print("Bye bye")
            sys.exit()
                    
##main code

def loop():
        
        g=Sensor()
        counter=0
        LOOP_TIME=0.05
        try:
               while True:
                     start_time=time.time()
                     value=g.get_value()
                     g.update_LED(value)
                     g.process_sample(start_time, np.mean(value))
                     now=time.time()
                     foo=LOOP_TIME-(now-start_time)
                     if foo>0:
                          time.sleep(foo)
                     if counter>15:
                         g.print_buffer()
                         counter=0
                     counter+=1
                     
        except (KeyboardInterrupt, SystemExit):
               pass
               g.finish()

def test():
    s = Sensor()

# for playback we can specify
#   sleep=0.1 for a fixed period between samples
# or
#   realtime=True which will pause the time betweesn recorded sample timestamps.
# otherwise the playback will be as fast as possible.
    t = TimeBuffer(size=6000, settings={"LOG_LEVEL":0})
    print("loading buffer")
    t.load('CSVs/sensor_play.csv')#sensor_play
    print("loaded data")
    
    t.play(s.process_sample, realtime=False)

if __name__ =="__main__":

        loop()
        #test()
        #g.loop()
       

