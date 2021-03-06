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
dots = dotstar.DotStar(board.SCK, board.MOSI, 64, brightness=0.25)
# MAIN LOOP

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

#print(color_pallete)

while True:
    pixels=[]

    pixels=np.array(amg.pixels).flatten()#np.squeeze(np.asarray(amg.pixels))
  
    i=0
    for pixel in pixels:       
        remap=interp(pixel,[16,30],[0,63]).astype(np.int)      
        colors=color_pallete[remap]
        dots[i] = (colors[0], colors[1], colors[2])
        i+=1
        
   # time.sleep(0.01);
    
   