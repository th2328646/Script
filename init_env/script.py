#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import re
import shutil
import commands

os.system('sh /home/init_dbdisk.sh')

cmds = ['mkfs.ext4 /dev/sdb1', "echo '/dev/sdb1 /data ext4 defaults 0 0 /' >> /etc/fstab", 'mkdir /data',
        'mount /dev/sdb1']


def init_dbdisk():
    for cmd in cmds:
        os.system(cmd)
    print 'successfully initialized.'


init_dbdisk()

start_cmd = 'systemctl start firewalld'
enable_cmd = 'systemctl enable firewalld'
disable_cmd = 'systemctl disable firewalld'
reload_cmd = 'firewall-cmd --reload'
port_add = 'firewall-cmd --permanent --zone=public --add-port=%s'
port_check = 'firewall-cmd --zone=public --query-port=%s'
port_list = ['8080/tcp', '8080/udp', '8443/tcp']


def start_firewall():
    chkstatus = commands.getoutput("systemctl status firewalld|grep -A 1 'Loaded'")
    if re.search('inactive', chkstatus):
        b = subprocess.call(start_cmd, shell=True)
        if b == 0:
            print "firewall started successfully."
    if re.search('firewalld.service; disabled', chkstatus):
        c = subprocess.call(enable_cmd, shell=True)
        if c == 0:
            print "firewall enabled successfully."


def port_conf():
    for port in port_list:
        chkport = commands.getoutput(port_check % port)
        if chkport == 'no':
            addport = commands.getoutput(port_add % port)
            if addport == 'success':
                print 'port %s added successfully.' % port
        else:
            print 'port %s has existed.' % port
    if os.system('firewall-cmd --reload'):
        print 'firewall reloaded successfully.'


start_firewall()
port_conf()

# download_urls = ["wget http://mirror.cogentco.com/pub/apache/tomcat/tomcat-8/v8.0.32/bin/apache-tomcat-8.0.32.tar.gz",'''wget --no-cookies --no-check-certificate --header "Cookie:oraclelicense=accept-securebackup-cookie;" http://download.oracle.com/otn-pub/java/jdk/8u73-b02/jdk-8u73-linux-x64.rpm''']
# env_path = "/root/temp"
#
#
# def download():
#	if not os.path.exists(env_path):
#		os.mkdir(env_path)
#	os.chdir(env_path)
#	for url in download_urls:
#		job = url.split('/')
#		i = len(job)
#		if not os.path.exists(job[i-1]):
#			code = subprocess.call(url, shell=True)
#			if code == 0 :
#				print "success.job is %s." % job[i-1]
#
# download()
#
install_cmds = ['rpm -ivh jdk-8u73-linux-x64.rpm', 'tar -zxf apache-tomcat-8.0.32.tar.gz']
download_path = "/root/temp"


def install_jdk_tomcat():
    os.chdir(download_path)
    for command in install_cmds:
        code = subprocess.call(command, shell=True)
        if code == 0:
            if re.search('jdk', command):
                print 'successfully installed jdk8.'
            else:
                print 'successfully installed tomcat8.'


yum_cmd = 'yum -y install %s '
install_list = ['unzip', 'epel-release', 'redis']


def install_unzip_redis():
    for install in install_list:
        cmd = yum_cmd % install
        if subprocess.call(cmd, shell=True) == 0:
            print 'successfully installed %s' % install


def redis_conf():
    os.system('systemctl enable redis')
    os.system('systemctl start redis')
    os.system('systemctl status redis')


install_jdk_tomcat()
install_unzip_redis()
redis_conf()


def addusr():
    addusr_cmds = ['groupadd tomcat', 'useradd -r tomcat -s /bin/false -g tomcat']
    for cmd in addusr_cmds:
        os.system(cmd)
        if re.match('groupadd', cmd):
            print 'groupadd successfully.'
        else:
            print 'useradd successfully.'


addusr()

ln_source = ['/data/opt/apache-tomcat-8.0.32/', '/data/opt/tomcat/logs', '/data/peihu/image/', '/data/peihu/html/']
ln_target = ['/data/opt/tomcat', '/home/tomcat', '/data/peihu/webapps', '/data/peihu/webapps']
makedirs = ['/data/opt', '/data/peihu', '/home/tomcat', '/data/peihu/image', '/data/peihu/html', '/data/peihu/webapps']


def link():
    # create new path. #
    for dirs in makedirs:
        if os.path.exists(dirs):
            print '%s has existed.' % dirs
        else:
            os.makedirs(dirs)
            print 'successfully makedir %s.' % dirs
    # move apache-tomcat-8.0.32 to '/data/opt'. #
    if not os.path.exists(ln_source[0]):
        shutil.move('/root/temp/apache-tomcat-8.0.32', '/data/opt')
    # create new symbolic link. #
    i = 0
    for i in range(0, len(ln_source)):
        cmd = 'ln -s %s %s' % (ln_source[i], ln_target[i])
        code = subprocess.call(cmd, shell=True)
        if code == 0:
            print 'successfully linked %s to %s.' % (ln_source[i], ln_target[i])
        i = i + 1
    # get uid and gid. #
    uid = int(commands.getoutput('id -u tomcat'))
    gid = int(commands.getoutput('id -g tomcat'))
    # change user rights. #
    os.chown('/home/tomcat', uid, gid)
    os.chown('/data/opt/tomcat/', uid, gid)
    # remove "/data/opt/tomcat/webapps/*". #
    if os.path.exists('/data/opt/tomcat/webapps/'):
        os.system('rm -f /data/opt/tomcat/webapps/*')


link()
