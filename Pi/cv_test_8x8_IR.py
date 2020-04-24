import cv2
import numpy as np
import time
import busio
import board
import adafruit_amg88xx
i2c = busio.I2C(board.SCL, board.SDA)
amg = adafruit_amg88xx.AMG88XX(i2c)#had to modify smbus.py
#        reg = c_uint8(int.from_bytes(cmd, byteorder='big', signed=False)

color_palette=[ 
 [ 255 , 0 , 0 ],
 [ 247 , 8 , 0 ],
 [ 239 , 16 , 0 ],
 [ 231 , 24 , 0 ],
 [ 223 , 32 , 0 ],
 [ 215 , 40 , 0 ],
 [ 207 , 48 , 0 ],
 [ 199 , 56 , 0 ],
 [ 191 , 64 , 0 ],
 [ 183 , 72 , 0 ],
 [ 175 , 80 , 0 ],
 [ 167 , 88 , 0 ],
 [ 159 , 96 , 0 ],
 [ 151 , 104 , 0 ],
 [ 143 , 112 , 0 ],
 [ 135 , 120 , 0 ],
 [ 128 , 128 , 0 ],
 [ 120 , 135 , 0 ],
 [ 112 , 143 , 0 ],
 [ 104 , 151 , 0 ],
 [ 96 , 159 , 0 ],
 [ 88 , 167 , 0 ],
 [ 80 , 175 , 0 ],
 [ 72 , 183 , 0 ],
 [ 64 , 191 , 0 ],
 [ 56 , 199 , 0 ],
 [ 48 , 207 , 0 ],
 [ 40 , 215 , 0 ],
 [ 32 , 223 , 0 ],
 [ 24 , 231 , 0 ],
 [ 16 , 239 , 0 ],
 [ 8 , 247 , 0 ],
 [ 0 , 255 , 0 ],
 [ 0 , 247 , 8 ],
 [ 0 , 239 , 16 ],
 [ 0 , 231 , 24 ],
 [ 0 , 223 , 32 ],
 [ 0 , 215 , 40 ],
 [ 0 , 207 , 48 ],
 [ 0 , 199 , 56 ],
 [ 0 , 191 , 64 ],
 [ 0 , 183 , 72 ],
 [ 0 , 175 , 80 ],
 [ 0 , 167 , 88 ],
 [ 0 , 159 , 96 ],
 [ 0 , 151 , 104 ],
 [ 0 , 143 , 112 ],
 [ 0 , 135 , 120 ],
 [ 0 , 128 , 128 ],
 [ 0 , 120 , 135 ],
 [ 0 , 112 , 143 ],
 [ 0 , 104 , 151 ],
 [ 0 , 96 , 159 ],
 [ 0 , 88 , 167 ],
 [ 0 , 80 , 175 ],
 [ 0 , 72 , 183 ],
 [ 0 , 64 , 191 ],
 [ 0 , 56 , 199 ],
 [ 0 , 48 , 207 ],
 [ 0 , 40 , 215 ],
 [ 0 , 32 , 223 ],
 [ 0 , 24 , 231 ],
 [ 0 , 16 , 239 ],
 [ 0 , 8 , 247 ]]

while True:
    rows = []
    print(np.array(amg.pixels))
    img8x8 = np.array(color_palette)[np.interp(np.array(amg.pixels),[10,30],[0,63]).astype(np.int)].astype(np.float)
    #print(img8x8,"\n")
    #img256x256 = cv2.resize(img8x8, (256, 256))
    #cv2.imshow('thermal', img256x256)
    #cv2.waitKey(1)
    #time.sleep(0.5)