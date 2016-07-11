import re,os,linecache,smtplib,time


def get_filename():
	time_list = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()).split(' ')
	catalina_name = 'catalina.'+time_list[0]+'.log'
	errlog_name = 'errlog.'+time_list[0]+'.txt'
	return (catalina_name, errlog_name)


def catch_err(filename):
#	filename_list = list(filename)
	today_catalina = list(filename)[0]
	today_errlog = list(filename)[1]
	f1 = open('/home/catalina/record.txt','r')
	content1 = f1.read()
	cursor = int(content1.split(',')[1])
	if cursor == 0:
		start_line = 1
	else:
		start_line = cursor
	infos = linecache.getlines('/home/catalina/%s' % today_catalina)[start_line:]
	errlog_path = '/home/catalina/%s' % today_errlog
	if not os.path.isfile(errlog_path):
		os.system('touch %s' % errlog_path)
	x=1
	for info in infos:
		error = re.search('ERROR',info)
		if error:
			cmd1 = '''echo "%s" >> %s''' % (info,errlog_path)
			os.system(cmd1)
			for err_info in infos[x:]:
				if not re.search(r'\b\d\d:\d\d:\d\d\b',err_info):
					cmd2 = '''echo "%s" >> %s''' % (err_info,errlog_path)
					os.system(cmd2)
				else:
					cmd3 = "echo '\n----------------------------------------------------------------------------------------------------------------------------------------------------------------\n' >> %s" % errlog_path
					os.system(cmd3)
					break
		x = x+1
		start_line = start_line+1
	time = os.stat('%s' % errlog_path).st_mtime
	return (time,start_line)


def change_record(answer):
	# get last mtime and err_log.txt end cursor. #
	f2 = open('record.txt','r')
	content2 = f2.read()
	last_tl_list = content2.split(',')	
	last_mod_time = str(last_tl_list[0])
	last_line_num = last_tl_list[1]
	# get this mtime and err_log.txt end cursor. #
	this_tl_list = list(answer)
	this_mod_time = str(this_tl_list[0])
	this_line_num = this_tl_list[1]
	if last_mod_time != this_mod_time:
		print "send email."
#		send_email()
	# change the time.txt about mtime and cursor. #
	last_mod_time = this_mod_time
	f3 = open('record.txt','w')
	time_line = last_mod_time+','+str(this_line_num)
	f3.write(time_line)


#sender = '591260005@qq.com'
#receivers = ['591260005@qq.com']
#
#def send_email():
#	message = """From: From Person <%s>
#		To: To Person <%s>
#		Subject: SMTP e-mail test
#
#		This is a test e-mail message.
#			""" % (sender,receivers)
#	try:
#		smtpObj = smtplib.SMTP()
#		smtpObj.connect('smtp.exmail.qq.com',25)
#		smtpObj.login('591260005@qq.com', 'baoyu0707...')
#		smtpObj.sendmail(sender, receivers, message)
#		smtpObj.close()
#		print "Successfully sent email."
#	except Exception, e:
#		print str(e)
#

change_record(catch_err(get_filename()))



