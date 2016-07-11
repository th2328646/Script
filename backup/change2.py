#!/usr/bin/python
#filename change2.py

import os
import time

class back_up: 
  def backup(self,source):
    print 'Please enter a target_dir:',
    target=raw_input()
    now=time.strftime('%Y%m%d-%H%M%S')
    target_dir=target+os.sep+now+'.zip'
    print target_dir
    zip_command="zip -qr %s %s"%(target_dir,source)
    print zip_command
    if os.system(zip_command)==0:
      print('Successfully backed up to %s.')%(target_dir)
    else:
      print('Backup failed.')

