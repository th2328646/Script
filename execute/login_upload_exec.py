#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import paramiko


def login_upload_execute():
    print 'Please input the hostinformation path:'
    path = raw_input()
    openfile = open(path, 'r')
    infors = openfile.readlines()
    for infor in infors:
        a = infor.split(',')
        ip = a[0]
        port = int(a[1])
        username = a[2]
        passwd = a[3].strip()
        upload(ip, port, username, passwd)
        login_execute(ip, port, username, passwd)
        #		execute()
        print '%s login_upload_execute success.' % ip


def login_execute(ip, port, username, passwd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port, username, passwd, timeout=3600)
    cmds = ['mkdir /root/temp', 'mv /home/apache-tomcat-8.0.32.tar.gz /root/temp',
            'mv /home/jdk-8u73-linux-x64.rpm /root/temp', 'python /home/script.py']
    for cmd in cmds:
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print stdout.read()
    ssh.close()


def upload(ip, port, username, passwd):
    local_path = '/home/init_env/'
    remote_path = '/home/'
    t = paramiko.Transport((ip, port))
    t.connect(username=username, password=passwd)
    sftp = paramiko.SFTPClient.from_transport(t)
    files = os.listdir(local_path)
    print files
    for f in files:
        print 'Uploading %s to %s.ip is %s.' % (f, os.path.join(remote_path, f), ip)
        sftp.put(os.path.join(local_path, f), os.path.join(remote_path, f))
    t.close()
    print 'upload successfully.'


if __name__ == "__main__":
	login_upload_execute()
