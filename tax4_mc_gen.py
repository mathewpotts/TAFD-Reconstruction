#!/usr/bin/env python3
# Author: Matt Potts

from multiprocessing import Pool
import re
import os
import sys
import glob
import random as r
import argparse

class tax4MCgen:
    def __init__(self,det):
        self.det = det
        self.detin = det[:2]
        if det == 'mdtax4':
            self.det_id = 37
            self.FD_ID = 7
        elif det == 'brtax4':
            self.det_id = 38
            self.FD_ID = 8
        else:
            print(f"{det} isn't mdtax4 or brtax4. Try again.")
            sys.exit(1)
        self.pass0_path=f'/home/tamember/data/{det}/pass0/data'
        self.mc_path=f'/home/tamember/data/{det}/mc'
        self.ot_path=f'/home/tamember/data/{det}/ontime'

    def setNr(self,Emin,Emax):
        setNr=[]
        for file in glob.glob(f'{self.pass0_path}/*/*fraw1*'):
            date = file.split('/')[-2] # date of data
            part = re.findall('p\d+.',file)[0][2:-1] # part number of data
            perc_ot = self.get_ot_mins(date,part)/20 # ot_mins/20 (parts are 20 mins long)
            setNr.append([date+part,Emin,Emax,perc_ot])
        return setNr

    def setNr_range(self,date_list,Emin,Emax):
        start=date_list[0]
        end=date_list[1]
        setNr_range=[]
        for date in range(start,end):
            if os.path.isdir(f'{self.pass0_path}/{date}'):
                for file in glob.glob(f'{self.pass0_path}/{date}/*fraw1*'):
                    date = file.split('/')[-2] # date of data
                    part = re.findall('p\d+.',file)[0][2:-1] # part number of data
                    perc_ot = self.get_ot_mins(date,part)/20 # ot_mins/20 (parts are 20 mins long) 
                    setNr_range.append([date+part,Emin,Emax,perc_ot])
        return setNr_range

    def get_ot_mins(self,date,part):
        filename = 'y' + date[:4] + 'm' + date[4:6] + 'd' + date[6:8] + 'p0' + part + '.ontime.' + self.det + '.txt'
        path = self.ot_path + '/' + date + '/' + filename
        line = open(path).readlines()[0]
        times = [idx for idx in line.split(' ') if idx != '']
        ot_mins = (int(times[1]) - int(times[0]))/60
        return ot_mins

    def iseed(self,setNr):
        seed=[]
        for idx in range(0,len(setNr)):
            seed.append("-" + str(r.randint(0,9)) + setNr[idx][0][2:])
        return seed

    def make_dirs(self,setNr):
        for idx in range(0,len(setNr)):
            #print('{0}/{1}'.format(self.mc_path,setNr[idx][0][:-2]))
            os.system("mkdir -p {0}/{1}/pass0 {0}/{1}/pass2 {0}/{1}/pass3 {0}/{1}/pass4 {0}/{1}/pass5 {0}/{1}/infile {0}/{1}/log".format(self.mc_path,setNr[idx][0][:-2]))

    def make_infile(self,setNr,iseed,spec_idx,nevents):
        for idx in range(0,len(setNr)):
            mod_nevents = int(setNr[idx][3] * nevents)
            txt=f'''          output file:  ./pr.{setNr[idx][1]}-{setNr[idx][2]}.tax4{self.detin}_mc.out
                setNr:  {setNr[idx][0]}
               use DB:  YES
                iseed:  {iseed[idx]}
             detector:  ta_{self.detin}_tax4.conf
         shift origin:  YES
                 nevt:  {mod_nevents}
           event type:  SHOWER
          iopt_spectr:  1
                gamma:  {spec_idx}
             minEnrgy:  {setNr[idx][1]}
             maxEnrgy:  {setNr[idx][2]}
              primary:  qgsjetii-03,proton
                rpmin:  100.0000000000000    
                rpmax:  50000.000000000000    
               thesh1:  0.000000000000000    
               thesh2:  1.22173048
               phish1:  -3.141592653589793    
               phish2:  3.141592653589793    
                dxlim:  2000.000000000000    
                hceil:  47000.00000000000
            '''
            print(txt,file=open(f'{self.mc_path}/{setNr[idx][0][:-2]}/infile/pr.{setNr[idx][1]}-{setNr[idx][2]}.p{setNr[idx][0][-2:]}.tax4{self.detin}_mc.in','w'))

    def gen_mc(self,setNr):
        # Get last date of gdas files for db support
        path=os.environ['UTAFD_RESOURCES_DIR'] + '/required/TA_Calib/gdas'
        last_gdas_file=os.popen('ls %s| tail -n1' % path).read()
        last_gdas_date=os.popen("dstdump {0}/{1} 2>/dev/null | grep FROM | tail -n1 | awk '{{print $2}}' | sed 's/\///g'".format(path,last_gdas_file[:-1])).read()

        # Only run if it is before last gdas date
        if setNr[0][:-2] <= last_gdas_date[:-1]: 
            path=f'{self.mc_path}/{setNr[0][:-2]}'
            cmds=''' 
            echo "mc2k12_main processing {0} part {1}"; mc2k12_main -o {0}/pass0/pr.{2}-{3}.p{1}.tax4{4}_mc.dst {0}/infile/pr.{2}-{3}.p{1}.tax4{4}_mc.in >& {0}/log/1.p{1}.io; 
            echo "stps2_main processing {0} part {1}"; stps2_main -det {5} -o {0}/pass2/pr.{2}-{3}.p{1}.tax4{4}_mc.ps2.dst {0}/pass0/pr.{2}-{3}.p{1}.tax4{4}_mc.dst >& {0}/log/2.p{1}.io; 
            echo "stpln_main processing {0} part {1}"; stpln_main -det {5} -o {0}/pass3/pr.{2}-{3}.p{1}.tax4{4}_mc.ps3.dst {0}/pass2/pr.{2}-{3}.p{1}.tax4{4}_mc.ps2.dst >& {0}/log/3.p{1}.io; 
            echo "stgeo_main processing {0} part {1}"; stgeo_main -det {5} -fit_type 4 -o {0}/pass4/pr.{2}-{3}.p{1}.tax4{4}_mc.ps4.dst {0}/pass3/pr.{2}-{3}.p{1}.tax4{4}_mc.ps3.dst >& {0}/log/4.p{1}.io; 
            echo "stpfl12_main processing {0} part {1}"; dev_stpfl12_main -det {5} -db -fit {6} -xm 650,700,750,800,850,900 -o {0}/pass5/pr.{2}-{3}.p{1}.tax4{4}_mc.ps5.dst {0}/pass4/pr.{2}-{3}.p{1}.tax4{4}_mc.ps4.dst >& {0}/log/5.p{1}.io;
            '''.format(path,setNr[0][-2:],setNr[1],setNr[2],self.detin,self.det_id,self.FD_ID)
            print(cmds,file=open('%s/process_file_%s.sh' % (path,setNr[0][-2:]),'w'))
            os.system('chmod +x %s/process_file_%s.sh' % (path,setNr[0][-2:]))
            os.system('cmd="%s/process_file_%s.sh";/bin/bash -c "$cmd"' % (path,setNr[0][-2:]))
    
    def check_logs(self,setNr):
        # check log files for memory errors causing pass5 not to execute
        date = setNr[0][:-2]
        part = setNr[0][-2:]
        filename = '5.p' + part + '.io'
        path = self.mc_path + '/' + date + '/log/' + filename
        return True
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate MC for a date range that exist in the pass0 directory')
    parser.add_argument('date_range',metavar='YYYYMMDD', type=int, nargs=2,help='Enter Start date YYYYMMDD and end date YYYYMMDD. Using -a flag then makes these dummy arguments')
    parser.add_argument('-det',metavar='detector',help='(mdtax4/brtax4)',required=True)
    parser.add_argument('-a',action='store_true',default=False,help='Generate MC for all files in the pass0 directory.')
    parser.add_argument('-Emin',metavar='minEnrgy',default='1E+17',help='Minimum thrown energy. Defaults to 1E+17 eV. (example -Emin 1E+17')
    parser.add_argument('-Emax',metavar='maxEnrgy',default='1E+21',help='Maximum thrown energy. Defaults to 1E+21 eV. (example -Emax 1E+21')
    parser.add_argument('-spec',metavar='gamma',default=2,help="Set the spectral index of the power spectrum. Defaults to E^-2. DON'T USE E^-1. (example -spec 2.92)")
    parser.add_argument('-n',metavar='nevts',type=int,default=20000,help='Set the number of events thrown in the MC. (example -n 20000)')
    args = parser.parse_args()
    tax4mc = tax4MCgen(args.det)
    
    if args.a == True:
        Nr=tax4mc.setNr(args.Emin,args.Emax)
        seed=tax4mc.iseed(Nr)
        tax4mc.make_dirs(Nr)
        tax4mc.make_infile(Nr,seed,args.spec,args.n)
        with Pool(4) as pool:
            pool.map(tax4mc.gen_mc,Nr)

    if args.a == False:
        print('Generating MC from %s to %s' % (args.date_range[0],args.date_range[1]))
        # Set the second argument of the argument list so that it works with range function if both date inputs are the same
        if args.date_range[0] == args.date_range[1]:
            args.date_range[1]=args.date_range[1]+1
        Nr=tax4mc.setNr_range(args.date_range,args.Emin,args.Emax)
        seed=tax4mc.iseed(Nr)
        tax4mc.make_dirs(Nr)
        tax4mc.make_infile(Nr,seed,args.spec,args.n)
        with Pool(4) as pool:
            pool.map(tax4mc.gen_mc,Nr)
       

