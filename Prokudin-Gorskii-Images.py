# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 08:16:44 2020

@author: hatam
"""

#channel 1= blue
#channel 2= green
#channel 3= red
import numpy as np
import cv2

#Function 
def find_delta (channel1,channel2,flagx,flagy,deltax,deltay):
    minBG=np.sum(abs(channel1 - channel2),dtype='int64')
    for i in range(-deltax,deltax,1):      #find delta in pyramid3
      for j in range(-deltay,deltay,1):
        mask_1=np.roll(channel2,2*flagx + i ,axis= 1)
        mask_1=np.roll(mask_1, j + 2* flagy , axis=0) 
        difference1 =np.sum(abs(channel1 - mask_1),dtype='int64') 
        if difference1< minBG:     # find range delta x & y in pyramid 1
              minBG=difference1
              flagxfinal= 2*flagx +i
              flagyfinal=2*flagy +j
    return flagxfinal , flagyfinal
              

img = cv2.imread('melons.tif',cv2.IMREAD_ANYDEPTH) # read 16-bit image


if len(img)%3==1:      # number of row%3==0
      img=np.append(img,np.zeros_like(img[0:2,:]) , axis=0)
elif len(img)%3==2:
   img=np.append(img,np.zeros_like(img[0:1,:]) , axis=0)

                
 #seprate image to three section                
channel_blue=img[0:int(len(img)/3),:].copy()
channel_green=img[int(len(img)/3):int(2*len(img)/3),:].copy()
channel_red=img[int(2*len(img)/3):int(len(img)),:].copy()

# convert to int number
channel_blue=channel_blue.astype('int32')
channel_green=channel_green.astype('int32')
channel_red=channel_red.astype('int32')


#creat image pyramid

#delete 1/2 of row and coloum image size 1/4
channel_blue_pyramid1=np.delete(channel_blue, np.s_[::2], 1)
channel_blue_pyramid1=np.delete(channel_blue_pyramid1, np.s_[::2], 0)
channel_green_pyramid1=np.delete(channel_green, np.s_[::2], 1)
channel_green_pyramid1=np.delete(channel_green_pyramid1, np.s_[::2], 0)
channel_red_pyramid1=np.delete(channel_red, np.s_[::2], 1)
channel_red_pyramid1=np.delete(channel_red_pyramid1, np.s_[::2], 0)

#delete 1/4 of row and coloum image size 1/16
channel_blue_pyramid2=np.delete(channel_blue_pyramid1 ,np.s_[::2], 1)
channel_blue_pyramid2=np.delete(channel_blue_pyramid2, np.s_[::2], 0)
channel_green_pyramid2=np.delete(channel_green_pyramid1, np.s_[::2], 1)
channel_green_pyramid2=np.delete(channel_green_pyramid2, np.s_[::2], 0)
channel_red_pyramid2=np.delete(channel_red_pyramid1, np.s_[::2], 1)
channel_red_pyramid2=np.delete(channel_red_pyramid2, np.s_[::2], 0)

#delete 1/8 of row and coloum image size 1/64
channel_blue_pyramid3=np.delete(channel_blue_pyramid2, np.s_[::2], 1)
channel_blue_pyramid3=np.delete(channel_blue_pyramid3, np.s_[::2], 0)
channel_green_pyramid3=np.delete(channel_green_pyramid2, np.s_[::2], 1)
channel_green_pyramid3=np.delete(channel_green_pyramid3, np.s_[::2], 0)
channel_red_pyramid3=np.delete(channel_red_pyramid2, np.s_[::2], 1)
channel_red_pyramid3=np.delete(channel_red_pyramid3, np.s_[::2], 0)

# find delta x & y  in green channel : take blue channel fixed

flag_x3=0
flag_y3=0
flag_x3 , flag_y3=find_delta (channel_blue_pyramid3,channel_green_pyramid3,flag_x3,flag_y3,25,25)
            
  
flag_x2 , flag_y2 =find_delta (channel_blue_pyramid2,channel_green_pyramid2,flag_x3,flag_y3,10,10)


flag_x1 , flag_y1 =find_delta (channel_blue_pyramid1,channel_green_pyramid1,flag_x2,flag_y2,10,10)


flag_x , flag_y =find_delta (channel_blue,channel_green,flag_x1,flag_y1,10,10)

 # find delta x & y in red channel : take blue channel fixed

flag_x3_r=0
flag_y3_r=0
flag_x3_r , flag_y3_r =find_delta (channel_blue_pyramid3,channel_red_pyramid3,flag_x3_r,flag_y3_r,25,25)

       
flag_x2_r , flag_y2_r =find_delta (channel_blue_pyramid2,channel_red_pyramid2,flag_x3_r,flag_y3_r,10,10)           


flag_x1_r , flag_y1_r =find_delta (channel_blue_pyramid1,channel_red_pyramid1,flag_x2_r,flag_y2_r,10,10)


flag_x_r , flag_y_r =find_delta (channel_blue,channel_red,flag_x1_r,flag_y1_r,10,10)

     
print("change green channel:",flag_x,flag_y)   
print("change red channel:",flag_x_r,flag_y_r)
# convert to range[0:255]
channel_blue=channel_blue/256    
channel_blue=channel_blue.astype('uint8')

channel_green=channel_green/256
channel_green=channel_green.astype('uint8')

channel_red=channel_red/256
channel_red=channel_red.astype('uint8')

img1=np.zeros((len(channel_blue),len(channel_blue[0]),3))
img1[:,:,0]=channel_blue
img1[:,:,1]=np.roll(channel_green,flag_y ,axis=0)
img1[:,:,1]=np.roll(img1[:,:,1],flag_x ,axis= 1)
img1[:,:,2]=np.roll(channel_red,flag_y_r ,axis= 0)
img1[:,:,2]=np.roll(img1[:,:,2],flag_x_r ,axis= 1)

cv2.imwrite('res04.jpg',img1)
