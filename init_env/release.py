#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import commands
import time


def unzip_configuration():
    os.system('unzip /home/configuration-test.zip -d /home')
    print 'yes'


unzip_configuration()

oldlinks = ['/data/opt/tomcat/conf/server.xml', '/data/opt/tomcat/conf/log4j.properties',
            '/data/opt/tomcat/webapps/peihu.war']


def remove_oldlinks():
    for oldlink in oldlinks:
        rm_cmd = 'rm -rf %s' % oldlink
        os.system(rm_cmd)
        print 'remove %s successfully.' % oldlink


remove_oldlinks()

cp_source = ['/home/configuration-test/peihu/*', '/home/configuration-test/script/tomcat', '/home/peihu.war']
cp_target = ['/data/peihu/', '/etc/init.d', '/data/peihu/webapps/']


def copy_to_targetdir():
    for x in range(0, len(cp_source)):
        cmd = 'yes|cp -rf %s %s' % (cp_source[x], cp_target[x])
        os.system(cmd)
        print 'successfully copy %s to %s.' % (cp_source[x], cp_target[x])
    print 'yes'


copy_to_targetdir()

ln_source = ['/data/peihu/config/server.xml', '/data/peihu/config/log4j.properties', '/data/peihu/webapps/peihu.war']
ln_target = ['/data/opt/tomcat/conf/server.xml', '/data/opt/tomcat/conf/', '/data/opt/tomcat/webapps/peihu.war']


def link():
    # create new symbolic link. #
    for y in range(0, len(ln_source)):
        cmd = 'ln -s %s %s' % (ln_source[y], ln_target[y])
        code = subprocess.call(cmd, shell=True)
        if code == 0:
            print 'successfully linked %s to %s.' % (ln_source[y], ln_target[y])


link()

ch_owners = ['/data/opt/tomcat', '/data/peihu/', '/data/peihu/webapps']


def change_owners():
    # get uid and gid. #
    uid = int(commands.getoutput('id -u tomcat'))
    gid = int(commands.getoutput('id -g tomcat'))
    # change user owners. #
    for ch_owner in ch_owners:
        os.chown(ch_owner, uid, gid)
        print 'successfully change owners to %d/%d.' % (uid, gid)


change_owners()

ch_right_cmds = ['chmod 766 /etc/init.d/tomcat', 'chmod +x /etc/rc.d/rc.local']


def change_rights():
    for cmd in ch_right_cmds:
        os.system(cmd)
        print 'yes'
    # add '/etc/init.d/tomcat start' to /etc/rc.local. #
    os.system("echo '/etc/init.d/tomcat start' >> /etc/rc.d/rc.local")


change_rights()

remove_cmds = ['rm -rf /home/configuration-test_older.zip', 'rm -rf /home/configuration-test_older',
               'rm -rf /home/peihu_older.war']
move_cmds = ['mv /home/configuration-test.zip /home/configuration-test_older.zip',
             'mv /home/configuration-test /home/configuration-test_older', 'mv /home/peihu.war /home/peihu_older.war']


def remove_rename():
    # remove the files which uploaded last time and rename the files which uploaded this time to 'xxx_older'. #
    for remove_cmd in remove_cmds:
        os.system(remove_cmd)
    for move_cmd in move_cmds:
        os.system(move_cmd)


remove_rename()
