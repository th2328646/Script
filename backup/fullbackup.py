#!/usr/bin/python
#filename fullbackup.py

import os
import time

class fullbackup
  def full_backup():
    print 'Please enter a target_path:',
    target_path=raw_input()
    print 'please enter the filename:',
    filename=raw_input()
    path=target_path+filename
    command='mysqldump --events --ignore-events --single-transaction --flush-lo\
gs --master-data=2 --all-databases > $s'%(path)
    if os.system(command)==0:
      print('Successfully full backup to %s!')%(path)
    else
      print('Backup failed!')   
