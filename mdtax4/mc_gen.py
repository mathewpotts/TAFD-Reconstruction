#!/usr/bin/env python3

from multiprocessing import Pool
import os
import sys
import glob
import argparse

def setNr(Emin,Emax):
    pass0_path='/home/tamember/matt/tax4md/work/pass0/data'
    setNr=[]
    for file in glob.glob('%s/*/*fraw1*' % pass0_path):
        date=file[43:51] # date of data
        part=file[65:67] # part number of data
        setNr.append([date+part,Emin,Emax])
    return setNr

def setNr_range(date_list,Emin,Emax):
    start=date_list[0]
    end=date_list[1]
    pass0_path='/home/tamember/matt/tax4md/work/pass0/data'
    setNr_range=[]
    for date in range(start,end):
        if os.path.isdir('%s/%s' % (pass0_path,date)):
            for file in glob.glob('%s/%s/*fraw1*' % (pass0_path,date)):
                date=file[43:51] # date of data
                part=file[65:67] # part number of data
                setNr_range.append([date+part,Emin,Emax])
    return setNr_range
                
def iseed(setNr):
    seed=[]
    for idx in range(0,len(setNr)):
        seed.append("-8"+ setNr[idx][0][2:])
    return seed

def make_dirs(setNr):
    for idx in range(0,len(setNr)):
        os.system('mkdir -p /home/tamember/matt/tax4md/work/mc/%s/pass0' % setNr[idx][0][:-2])
        os.system('mkdir -p /home/tamember/matt/tax4md/work/mc/%s/pass2' % setNr[idx][0][:-2])
        os.system('mkdir -p /home/tamember/matt/tax4md/work/mc/%s/pass3' % setNr[idx][0][:-2])
        os.system('mkdir -p /home/tamember/matt/tax4md/work/mc/%s/pass4' % setNr[idx][0][:-2])
        os.system('mkdir -p /home/tamember/matt/tax4md/work/mc/%s/pass5' % setNr[idx][0][:-2])
        os.system('mkdir -p /home/tamember/matt/tax4md/work/mc/%s/infile' % setNr[idx][0][:-2])
        os.system('mkdir -p /home/tamember/matt/tax4md/work/mc/%s/log' % setNr[idx][0][:-2])

def make_infile(setNr,iseed,spec_idx,nevents):
    for idx in range(0,len(setNr)):
        txt='''      output file:  ./pr.{2}-{3}.tax4md_mc.out
            setNr:  {0}
           use DB:  YES
            iseed:  {1}
         detector:  ta_md_tax4.conf
     shift origin:  YES
             nevt:  {5}
       event type:  SHOWER
      iopt_spectr:  1
            gamma:  {4}
         minEnrgy:  {2}
         maxEnrgy:  {3}
          primary:  qgsjetii-03,proton
            rpmin:  100.0000000000000    
            rpmax:  50000.000000000000    
           thesh1:  0.000000000000000    
           thesh2:  1.22173048
           phish1:  -3.141592653589793    
           phish2:  3.141592653589793    
            dxlim:  2000.000000000000    
            hceil:  47000.00000000000
        '''.format(setNr[idx][0],iseed[idx],setNr[idx][1],setNr[idx][2],spec_idx,nevents)
        print(txt,file=open('/home/tamember/matt/tax4md/work/mc/{0}/infile/pr.{1}-{2}.p{3}.tax4md_mc.in'.format(setNr[idx][0][:-2],setNr[idx][1],setNr[idx][2],setNr[idx][0][-2:]),'w'))

def gen_mc(setNr):
    # Get last date of gdas files for db support
    path='/home/tamember/software/TA/UTAFD/resources/required/TA_Calib/gdas'
    last_gdas_file=os.popen('ls %s| tail -n1' % path).read()
    last_gdas_date=os.popen("dstdump {0}/{1} 2>/dev/null | grep FROM | tail -n1 | awk '{{print $2}}' | sed 's/\///g'".format(path,last_gdas_file[:-1])).read()

    # Only run if it is before last gdas date
    if setNr[0][:-2] <= last_gdas_date[:-1]: 
        path='/home/tamember/matt/tax4md/work/mc/%s' % setNr[0][:-2]
        cmds=''' 
        echo "mc2k12_main processing {0} part {1}"; mc2k12_main -o {0}/pass0/pr.{2}-{3}.p{1}.tax4md_mc.dst {0}/infile/pr.{2}-{3}.p{1}.tax4md_mc.in >& {0}/log/1.p{1}.io; 
        echo "stps2_main processing {0} part {1}"; stps2_main -det 37 -o {0}/pass2/pr.{2}-{3}.p{1}.tax4md_mc.ps2.dst {0}/pass0/pr.{2}-{3}.p{1}.tax4md_mc.dst >& {0}/log/2.p{1}.io; 
        echo "stpln_main processing {0} part {1}"; stpln_main -det 37 -o {0}/pass3/pr.{2}-{3}.p{1}.tax4md_mc.ps3.dst {0}/pass2/pr.{2}-{3}.p{1}.tax4md_mc.ps2.dst >& {0}/log/3.p{1}.io; 
        echo "stgeo_main processing {0} part {1}"; stgeo_main -det 37 -fit_type 4 -o {0}/pass4/pr.{2}-{3}.p{1}.tax4md_mc.ps4.dst {0}/pass3/pr.{2}-{3}.p{1}.tax4md_mc.ps3.dst >& {0}/log/4.p{1}.io; 
        echo "stpfl12_main processing {0} part {1}"; dev_stpfl12_main -det 37 -fit 3, -xm 685,720,755,790,825,860 -o {0}/pass5/pr.{2}-{3}.p{1}.tax4md_mc.ps5.dst {0}/pass4/pr.{2}-{3}.p{1}.tax4md_mc.ps4.dst >& {0}/log/5.p{1}.io;
        '''.format(path,setNr[0][-2:],setNr[1],setNr[2])
        print(cmds,file=open('%s/process_file_%s.sh' % (path,setNr[0][-2:]),'w'))
        os.system('chmod +x %s/process_file_%s.sh' % (path,setNr[0][-2:]))
        os.system('cmd="%s/process_file_%s.sh";/bin/bash -c "$cmd"' % (path,setNr[0][-2:]))
    
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate MC for a date range that exist in the pass0 directory')
    parser.add_argument('date_range',metavar='YYYYMMDD', type=int, nargs=2,help='Enter Start date YYYYMMDD and end date YYYYMMDD. Using -a flag then makes these dummy arguments')
    parser.add_argument('-a',action='store_true',default=False,help='Generate MC for all files in the pass0 directory.')
    parser.add_argument('-Emin',metavar='minEnrgy',default='1E+17',help='Minimum thrown energy. Defaults to 1E+17 eV. (example -Emin 1E+17')
    parser.add_argument('-Emax',metavar='maxEnrgy',default='1E+21',help='Maximum thrown energy. Defaults to 1E+21 eV. (example -Emax 1E+21')
    parser.add_argument('-spec',metavar='gamma',default=2,help="Set the spectral index of the power spectrum. Defaults to E^-2. DON'T USE E^-1. (example -spec 2.92)")
    parser.add_argument('-n',metavar='nevts',type=int,default=20000,help='Set the number of events thrown in the MC. (example -n 20000)')
    args = parser.parse_args()
    
    if args.a == True:
        Nr=setNr(args.Emin,args.Emax)
        seed=iseed(Nr)
        make_dirs(Nr)
        make_infile(Nr,seed,args.spec,args.n)
        with Pool(4) as pool:
            pool.map(gen_mc,Nr)

    if args.a == False:
        print('Generating MC from %s to %s' % (args.date_range[0],args.date_range[1]))
        # Set the second argument of the argument list so that it works with range function if both date inputs are the same
        if args.date_range[0] == args.date_range[1]:
            args.date_range[1]=args.date_range[1]+1
        Nr=setNr_range(args.date_range,args.Emin,args.Emax)
        seed=iseed(Nr)
        make_dirs(Nr)
        make_infile(Nr,seed,args.spec,args.n)
        with Pool(4) as pool:
            pool.map(gen_mc,Nr)
       

