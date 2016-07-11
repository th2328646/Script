#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

import paramiko


def make_choice():
    print '''Please make your choice:
	 ______________________________________________
	|                                 	           |
	|   1. release configuration and war package.  |
	|                                              |
	|   2. add or replace dirs.                    |
	|                                              |
	|   3. add or replace some files.              |
	|					                           |
	|   4. remove some files or dirs.              |
	|                                              |
	|   5. exit.                                   |
	|					                           |
	|______________________________________________|
	'''
    choice = raw_input()
    if choice == '1':
        release_conf_war()
        make_choice()
    elif choice == '2':
        upload_dir()
        make_choice()
    elif choice == '3':
        add_replace()
        make_choice()
    elif choice == '4':
        remove()
        make_choice()
    elif choice == '5':
        sys.exit(0)
    else:
        print 'Please make your choice.'


'''--------------------------------------------------------------------------------------------------------------------
------------------------------------'''


def release_conf_war():
    print "Please input the local path and split by ',':\n(like: /dir1/dir2/filename1,/dir3/filename2)"
    local_path = raw_input().split(',')
    print "Please input the remote path and split by ',':\n(like: /dir1/dir2/filename1,/dir3/filename2)"
    remote_path = raw_input().split(',')
    openfile = open('/home/execute/ip.txt', 'r')
    infors = openfile.readlines()
    for i in range(0, len(infors)):
        info_list = infors[i].split(',')
        args = list(get_hostinfo(info_list))
        release_dir(args[0], args[1], args[2], args[3], local_path, remote_path)
        release_cmd = 'python /home/release.py'
        login_execute(args[0], args[1], args[2], args[3], release_cmd)


def release_dir(ip, port, username, passwd, local_path, remote_path):
    t = paramiko.Transport((ip, port))
    t.connect(username=username, password=passwd)
    sftp = paramiko.SFTPClient.from_transport(t)
    for i in range(0, len(local_path)):
        files = os.listdir(local_path[i])
        mkdir_cmd = 'mkdir -p %s' % remote_path[i]
        login_execute(ip, port, username, passwd, mkdir_cmd)
        for f in files:
            print 'Uploading %s to %s.ip is %s.' % (f, os.path.join(remote_path[i], f), ip)
            sftp.put(os.path.join(local_path[i], f), os.path.join(remote_path[i], f))
    t.close()


'''-------------------------------------------------------------------------------------------------------------------
-------------------------------------'''


def upload_dir():
    print "Please input the local dir path and split by ',':\n(like: /dir1/dir2/,/dir3/dir4)"
    local_dir_path = raw_input().split(',')
    print "Please input the remote dir path and split by ',':\n(like: /dir1/dir2/,/dir3/)"
    remote_dir_path = raw_input().split(',')
    openfile = open('/home/execute/ip.txt', 'r')
    infors = openfile.readlines()
    for x in range(0, len(infors)):
        info_list = infors[x].split(',')
        args = list(get_hostinfo(info_list))
        t = paramiko.Transport((args[0], args[1]))
        t.connect(username=args[2], password=args[3])
        sftp = paramiko.SFTPClient.from_transport(t)
        for y in range(len(local_dir_path)):
            files = os.listdir(local_dir_path[y])
            mkdir_cmd = 'mkdir -p %s' % remote_dir_path[y]
            login_execute(args[0], args[1], args[2], args[3], mkdir_cmd)
            for f in files:
                print 'Uploading %s to %s.ip is %s.' % (f, os.path.join(remote_dir_path[y], f), args[0])
                sftp.put(os.path.join(local_dir_path[y], f), os.path.join(remote_dir_path[y], f))
        t.close()


'''--------------------------------------------------------------------------------------------------------------------
------------------------------------'''


def add_replace():
    print "Please input the local path and split by ',':\n(like: /dir1/dir2/filename1,/dir3/filename2)"
    local_path = raw_input().split(',')
    print "Please input the remote path and split by ',':\n(like: /dir1/dir2/filename1,/dir3/filename2)"
    remote_path = raw_input().split(',')
    openfile = open('/home/execute/ip.txt', 'r')
    infors = openfile.readlines()
    for i in range(0, len(infors)):
        info_list = infors[i].split(',')
        args = list(get_hostinfo(info_list))
        upload_file(args[0], args[1], args[2], args[3], local_path, remote_path)


def upload_file(ip, port, username, passwd, local_path, remote_path):
    t = paramiko.Transport((ip, port))
    t.connect(username=username, password=passwd)
    sftp = paramiko.SFTPClient.from_transport(t)
    for x in range(0, len(local_path)):
        mk_dir = os.path.dirname(remote_path[x])
        mkdir_cmd = 'mkdir -p %s' % mk_dir
        login_execute(ip, port, username, passwd, mkdir_cmd)
        sftp.put(local_path[x], remote_path[x])
        print 'Uploading %s to %s.ip is %s.' % (local_path[x], remote_path[x], ip)
    t.close()


'''--------------------------------------------------------------------------------------------------------------------
------------------------------------'''


def remove():
    print "Please input the files path you want to remove on the remote server and split by ',':\n(like : " \
          "/dir1/dir2/filename1,/dir3/filename2)"
    remote_path = raw_input().split(',')
    openfile = open('/home/execute/ip.txt', 'r')
    infors = openfile.readlines()
    for i in range(0, len(infors)):
        info_list = infors[i].split(',')
        args = list(get_hostinfo(info_list))
        for r_path in remote_path:
            rm_cmd = 'rm -rf ' + r_path
            login_execute(args[0], args[1], args[2], args[3], rm_cmd)
            print 'remove %s successfully.' % r_path


'''------------------------------------------------------------------------------------------------------------------
-------------------------------------'''


def get_hostinfo(info_list):
    ip = info_list[0]
    port = int(info_list[1])
    username = info_list[2]
    passwd = info_list[3].strip()
    return ip, port, username, passwd


def login_execute(ip, port, username, passwd, cmd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port, username, passwd, timeout=5)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print stdout.read()
    ssh.close()


if __name__ == "__main__":
    make_choice()
