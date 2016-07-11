import paramiko,os,time,threading

class ssh_client(threading.Thread):
#	def __init__(self, ip, commands):
	def __init__(self, ip):
		threading.Thread.__init__(self)
		self.ip = ip
#		self.commands = commands

	def run(self):
		t = paramiko.Transport((self.ip,22))
		t.connect(username='root',password='123456')
		sftp = paramiko.SFTPClient.from_transport(t)
		fs = os.listdir('/home/release')
		for f in fs:
			path1 = os.path.join('/home/release',f)
			path2 = os.path.join('/home',f)
			sftp.put(path1,path2)
		t.close()
	
	        client = paramiko.SSHClient()
	        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	        client.connect(self.ip,port=22,username='root',password='123456',timeout=5)
#		for command in commands:
#	        	stdin,stdout,stderr=client.exec_command(command.strip())
#	        	stdout.read()
#	        	stderr.read()
		stdin,stdout,stderr = client.exec_command('python /home/release.py')
	        client.close()
	
	def stop(self):
		self.thread_stop = True

if __name__=='__main__':
	start = time.clock()
	i = open('/home/choice/ip.txt','r')
	ip_list = i.readlines()
#	c = open('/home/choice/commands.txt','r')
#	commands = c.readlines()
	threads = []	
	for ip in ip_list:
#        	temp_thread = ssh_client(ip,commands)
		temp_thread = ssh_client(ip)
		threads.append(temp_thread)
	for thread in threads:
       		thread.start()
		thread.join()
	end = time.clock()
	print "%.03f" % (end-start)
