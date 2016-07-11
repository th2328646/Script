#!/usr/bin/python
#filename change.py

import os
import time

class incrementalbackup:
  def pipei(self):
    print 'Please enter a source_path:',
    source_path=raw_input()
    filenames=os.listdir(source_path)
    print filenames
    for files in filenames:
      splits=os.path.splitext(files)
      filename='mysql-bin'
      suffix=splits[1]
      if filename in splits:
        print files,suffix
        log=suffix[1:]
        today=source_path+os.sep+time.strftime('%Y%m%d') 
        if not os.path.exists(today):
          os.mkdir(today)
        files_path=source_path+os.sep+files
#        print files_path
        log_path=today+os.sep+'log'+log+'.txt'
#        print log_path
        change_command='mysqlbinlog %s>%s'%(files_path,log_path)
        if os.system(change_command)==0:
          print('Successfully %s changed to %s.')%(files_path,log_path)
        else:
          print('Change failed.')
    return today
 

#  def backup():
#    print 'Please enter a target_dir:',
#    target=raw_input()
#    now=time.strftime('%Y%m%d-%H%M%S')
#    target_dir=target+os.sep+now+'.zip'
#    print target_dir
#    zip_command="zip -qr %s %s"%(target_dir,today)
#    print zip_command
#    if os.system(zip_command)==0:
#      print('Successfully backed up to %s.')%(target_dir)
#    else:
#      print('Backup failed.')

  if __name__=='__main__':
    change()
    print today
#   backup() 

#  change()
#  backup()
