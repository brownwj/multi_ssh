import threading 
import time
import ssh

class ssh_client(threading.Thread):
    def __init__(self, ip, dirs):
        threading.Thread.__init__(self)
        self.ip = ip
        self.dirs = dirs

    def run(self):
        client = ssh.SSHClient()
        client.set_missing_host_key_policy(ssh.AutoAddPolicy())
        client.connect(self.ip,port=22,username='USERNAME',password='PASSWORD',timeout=4)
        stdin,stdout,stderr = client.exec_command("mkdir aaa")
        stdout.read()
        stderr.read()
        for key in self.dirs:
            sftp = client.open_sftp()
            print key,"=",self.dirs[key]
            sftp.put(key, self.dirs[key])
        client.close()

    def stop(self):
        self.thread_stop = True

if __name__=='__main__':
    ip_list = open('ip_list','r')
    copy_list = open('copy_list', 'r')
    dirs={}
    while True:
        temp_key = copy_list.readline().strip()
        if not temp_key:
            break;
        temp_value = copy_list.readline().strip()
        if not temp_value:
            print "line no is odd" 
        dirs[temp_key] = temp_value
    print dirs
    dirs.clear()
    dirs={"test.aaa":"hadoop-core/test.aaa","test.bbb":"hadoop-core/"}
    print dirs
    threads = []
    for ip in ip_list:
        temp_thread = ssh_client(ip, dirs)
        threads.append(temp_thread)
    for thread in threads:
        thread.start()
