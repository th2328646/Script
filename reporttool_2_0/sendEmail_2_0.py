#!/usr/bin/env python
# coding=utf-8

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from ConfigParser import ConfigParser
import smtplib
import subprocess
import time

CONFIGFILE = "report_service_2_0.ini"
config = ConfigParser()
config.read(CONFIGFILE)

time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
newExcelname = config.get("FILE", "_newExcelName")
finalExcelname = "gps_daily_report_" + time + ".xls"
subprocess.call(["mv", newExcelname, finalExcelname])

reportFrom = config.get("EMAILL", "_from")
reportPwd = config.get("EMAILL", "_pwd")

msg = MIMEMultipart()
msg["Subject"] = u"车辆定位平台日报_%s" % time
msg["From"] = reportFrom

part1 = MIMEText("此邮件由服务器于每日23:00自动发送，请勿回复！", 'html', 'utf-8')
msg.attach(part1)

part = MIMEApplication(open(finalExcelname, 'rb').read())
part.add_header('Content-Disposition', 'attachment', filename=finalExcelname)
msg.attach(part)

reportSmtp = config.get("EMAILL", "_smtp")
reportPort = config.getint("EMAILL", "_port")

fileDevList = open("email_list.txt")
allLines = fileDevList.readlines()
for line in allLines:
    to = line.rstrip()
    try:
        s = smtplib.SMTP(reportSmtp, timeout=reportPort)
        s.login(reportFrom, reportPwd)
        s.sendmail(reportFrom, to, msg.as_string())
        print "\n================已成功发送邮件至：< %s >================\n" % to
    except Exception, e:  
        print str(e)
fileDevList.close()

savePath = config.get("FILE", "_savePath")
subprocess.call(["mv", finalExcelname, savePath + finalExcelname])
