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
    f_bad=open('bad.csv','w')


## get shift index    
## should be 94 x 73
    shift_list=array.array('f', (0.0,) * (layer_count))
    surf_list=[]
    surf_i=0

#    f_surfs=open('FangModel/surfs','r')
    f_surfs=open('FangModel/ETOPO1.surfs','r')
    surfs=f_surfs.readlines()
    f_surfs.close()

## surf ranges from 3000 to -2045
## since model goes from -1.5k to 30k, need to shifts  
## for surf from 1500 to 3000, needs to shift as differences
    s_i=0
    top_cnt=0
    skip_cnt=0
    for s in surfs:
        dif=0
        surf=float(s.strip())
        surf_list.append(surf)
        t=(surf-1500)/500
        if(t > 0) :
          dif=math.floor(t)
          shift_list[s_i]=dif
          top_cnt=top_cnt+1
        else :
          ## skip for now
          skip_cnt=skip_cnt+1
        s_i=s_i+1
            
    print("max shift ",max(shift_list))
    print("min shift ",min(shift_list))
    print("max surf ",max(surf_list))
    print("min surf ",min(surf_list))
    print("top cnt", top_cnt)

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
            f_bad.write(oline)

          if(newz >= 0 and newz <= 31.5):
            nline=l[1]+","+l[0]+","+str(newz)+","+l[3]+","+l[4]
            f_new.write(nline)
            valid_cnt=valid_cnt +1
        shift_i = shift_i + 1

        if(shift_i == layer_count) :
          shift_i=0
  
    f_new.close()
    f_old.close()
    f_bad.close()

    print("total valid write count :",valid_cnt)
    print("                 out of :",total_count)

    print("\nDone!")

if __name__ == "__main__":
    main()


