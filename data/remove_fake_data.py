#!/usr/bin/env python

#
#  create SJFZ_Fangetal2019_VpandVs_clean.csv
#  from SJFZ_Fangetal2019_VpVsratio.csv
#
#
## For both models I sent a couple of weeks ago, we were using the sea 
## level as 0 km with positive depth downwards (e.g. -1.5 km would be 1.5 km
## above sea level).
## 
## (1) Are values above the free surface artificial, and should  be ignored?
## Yes. The program using a regular box that contains all events and stations,
## thus regions above the free surface are artificial.
## (2) How do you suggest separating the actual volume of the crust from 
## "artificial material" above it?
## I would use the real topography as a layer to mask those values; everything 
## above the topography should be removed. There will be some interpolation 
## problem, but with the resolution we have, it won't matter.
#
#
# His inversion using a a regular box as grids, so there are grids above the 
# free surface. Data at these grids are artificial (even if they have values 
# differ from ’special value’), so I removed them all using the topo data 
# (first figure below). Besides, layers with depth = -1,-0.5 are interpolated 
# from depth=0 and depth=1.5km, so I also remove them if the data at depth=-1.5km 
# is artificial.
#

import getopt
import sys
import subprocess
import struct
import numpy as np
import array
import os
import pdb

dimension_x =  94
dimension_y =  73
dimension_z =  64

def usage():
    print("\n./remove_fake_data.py\n\n")
    sys.exit(0)

def no_need_val(d_val,s_val) :
    if(d_val < s_val) :
      return 0
    else:
      return 1

#-118.17,32.38,-1.50,5.50,3.14
# to
#-118.17,32.38,-1.50,-9.999,-9.999
def rewrite_fake(oline):
    l=oline.split(",")
    nline=l[0]+","+l[1]+","+l[2]+","+"-9.999,-9.999\n"
    return nline

def main():
    total_count=dimension_x * dimension_y * dimension_z

## should be 94 x 73
    surf_list=[]
    f_surf=open('FangModel/surfs','r')
    surfs=f_surf.readlines()
    for s in surfs:
        sur=float(s.strip())
        surf_list.append(sur)
    f_surf.close()

    dep_list=[]
    f_depth=open('FangModel/depth','r')
    deps=f_depth.readlines()
    for z in deps:
        dep=float(z.strip())
        dep_list.append(dep)
    f_depth.close()

    f_old=open('FangModel/SJFZ_Fangetal2019_VpVsratio.csv','r')
    olds=f_old.readlines()
    f_new=open('FangModel/SJFZ_Fangetal2019_VpandVs_clean.csv','w')

    dep_i=0
    surf_i=0
    f_old_i=0;

    rewrite_cnt=0
    no_rewrite_cnt = 0
    track_fake_1.5 = []  ## should have 6862 of these
    

    d_val= -1.0 * (dep_list[dep_i]*1000) 
    for oline in olds:
        ## copy header
        if(f_old_i == 0) : 
          f_new.write(oline)
        else :
          s_val = surf_list[surf_i]
          if(surf_i == 0) : 
             print(dep_list[dep_i])
             print("  first one :",oline.strip())
          if no_need_val(d_val,s_val) :
          if( (dep_i > 0) && (dep_i <= 2) ) :
            if (track_fake_1.5[surf_i]==1) :
              nline=rewrite_fake(oline)
              f_new.write(nline)
              rewrite_cnt=rewrite_cnt+1
              continue 
          if no_need_val(d_val,s_val) :
            ## no change
            f_new.write(oline)
            if(dep_i == 0) :
              track_fake_1.5.append(0);
            no_rewrite_cnt=no_rewrite_cnt+1
          else:
            ## rewrite vp/vs to -9999.000
            nline=rewrite_fake(oline)
            if(dep_i == 0) :
              track_fake_1.5.append(1);
            f_new.write(nline)
            rewrite_cnt=rewrite_cnt+1
          surf_i=surf_i+1
          if(surf_i >= dimension_x * dimension_y) :
            print("  last one :",oline.strip())
            print("  no_rewrite_cnt :",no_rewrite_cnt," at ", d_val)
            no_rewrite_cnt=0
            surf_i=0;
            dep_i=dep_i+1
            if(dep_i < dimension_z) :
              d_val= -1.0 * (dep_list[dep_i]*1000) 
        f_old_i = f_old_i+1 

    print("total rewrite count :",rewrite_cnt)

    f_new.close()
    f_old.close()

    print("\nDone!")

if __name__ == "__main__":
    main()


