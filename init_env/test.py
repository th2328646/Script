import ssh

class ssh_client(threading.Thread):
    def __init__(self, ip, commands):
        threading.Thread.__init__(self)
        self.ip = ip
        self.commands = commands

    def run(self):
        client = ssh.SSHClient()
        client.set_missing_host_key_policy(ssh.AutoAddPolicy())
        client.connect(self.ip,port=22,username='USERNAME',password='PASSWORD',timeout=4)
        for command in self.commands:
            stdin,stdout,stderr=client.exec_command(command)
#            for std in stdout.readline():
#                print std;
            stdout.read()
            stderr.read()
        client.close()

    def stop(self):
        self.thread_stop = True

if __name__=='__main__':
    ip_list = open('ip_list','r')
    command_list = open('command_list','r')
    commands = []
    for each_command in command_list:
        commands.append(each_command)
    threads = []
    for ip in ip_list:
        temp_thread = ssh_client(ip, commands)
        threads.append(temp_thread)
    for thread in threads:
        thread.start()
