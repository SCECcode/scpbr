#!/usr/bin/env python

#
#  create SJFZ_Fangetal2019_VpandVs_clean.csv
#  from Fang_19_new.csv created by Hao
#  eliminate entry that is NA and also entry that got shifted out 
#  beyond 31.5km
#

import getopt
import sys
import subprocess
import struct
import numpy as np
import array
import os
import pdb
import math

dimension_x =  94
dimension_y =  73
dimension_z =  64

def usage():
    print("\n./rework_fang_data.py\n\n")
    sys.exit(0)

def main():
    total_count=dimension_x * dimension_y * dimension_z
    layer_count=dimension_x * dimension_y

    f_old=open('FangModel/Fang_19_new.csv','r')
    olds=f_old.readlines()
    f_new=open('FangModel/SJFZ_Fangetal2019_VpandVs_clean.csv','w')


## get shift index    
## should be 94 x 73
    shift_list=[]
    surf_list=[]
    surf_i=0
    cnt_n1500=0
    cnt_0=0
    cnt_m0=0

#    f_surf=open('FangModel/surfs','r')
    f_surf=open('FangModel/ETOPO1.surfs','r')
    surfs=f_surf.readlines()
    for s in surfs:
        dif=0
        sur=float(s.strip())
        surf_list.append(sur)
        t=(sur-1500)/500
        if(t > 0) :
          dif=math.floor(t)
          cnt_n1500=cnt_n1500+1
        else :
          t=(sur-0)/500
          if(t > 0) :
            dif=math.floor(t)
            cnt_0=cnt_0+1
          else :
            dif=math.ceil(t)
            cnt_m0=cnt_m0+1
        shift_list.append(dif)

            
    f_surf.close()
    print("max shift ",max(shift_list))
    print("min shift ",min(shift_list))
    print("max surf ",max(surf_list))
    print("min surf ",min(surf_list))
    print("cnt_n1500", cnt_n1500)
    print("cnt_0", cnt_0)
    print("cnt_m0", cnt_m0)

# shift, positive shift/shift down
#        negative z/shift  up
#          current value + (500)* shift

    header=1
    valid_cnt=0
    shift_i=0

    for oline in olds:
        ## copy header
        if(header) : ## skip first line 
          nline="longitude,latitude,depth,Vp,Vs\n"
          f_new.write(nline)
          header=0
          continue
#latitude,longitude,depth,Vp,Vs
#32.38,-118.17,-1.5,nan,nan
#to
#longitude,latitude,depth,Vp,Vs
#-118.17,32.38,-1.5,-9.999,-9.999
        l=oline.split(",")
        if(l[3] != "nan") :
          oldz=float(l[2])
          if(shift_list[shift_i] == 0): 
            newz=oldz
          else:
            newz=(oldz * 1000 + (500)* shift_list[shift_i])/1000
         
          if(newz < 0) :
            print("hum... newz less than 0")

          if(newz >= 0 and newz <= 31.5):
            nline=l[1]+","+l[0]+","+str(newz)+","+l[3]+","+l[4]
            f_new.write(nline)
            valid_cnt=valid_cnt +1
        shift_i = shift_i + 1

        if(shift_i == layer_count) :
          shift_i=0
  
    f_new.close()
    f_old.close()

    print("total valid write count :",valid_cnt)
    print("                 out of :",total_count)

    print("\nDone!")

if __name__ == "__main__":
    main()

