#!/usr/bin/env python

#
#  create Vp.dat and Vs.dat from
#  from SJFZ_Fangetal2016_VpandVs.csv
#


import getopt
import sys
import subprocess
import struct
import numpy as np
import array
import pdb

dimension_x =  94
dimension_y =  73
dimension_z =  16 

def usage():
    print("\n./create_data_inp_file.py\n\n")
    sys.exit(0)

def main():

    total_count=dimension_x * dimension_y * dimension_z
    count=0

    f_mats = open("Fang2016Model/SJFZ_Fangetal2016_VpandVs.csv")
    vptxt = open('fang_inp/Vp.dat','w')
    vstxt = open('fang_inp/Vs.dat','w')

    vp_arr = np.genfromtxt("Fang2016Model/SJFZ_Fangetal2016_VpandVs.csv",
          dtype=np.float32, delimiter=',', skip_header=1,filling_values=9999,usecols=4)
    vs_arr = np.genfromtxt("Fang2016Model/SJFZ_Fangetal2016_VpandVs.csv",
          dtype=np.float32, delimiter=',', skip_header=1,filling_values=9999,usecols=5)

    print(len(vp_arr))
    print(len(vs_arr))
## reshape them
    vp_3d=np.reshape(vp_arr,(dimension_z,dimension_y,dimension_x))
    print(len(vp_3d))
    print(len(vp_3d[0]))
    print(len(vp_3d[0][0]))
    print(vp_3d[0][0])
    sys.exit(0)

#    vptxt.write(vpline);
#    vstxt.write(vxline);

    vptxt.close()
    vstxt.close()

    print("\nDone!")

if __name__ == "__main__":
    main()


