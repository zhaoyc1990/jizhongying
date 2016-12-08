# coding:utf-8
#from host.models import hostinfo
import paramiko
import sys
import os
import time
import datetime
class LogSplit:
	def __init__(self, host, starttime, stoptime, srcfile, destfile, forwarding_host=None, conport=None, linenum=None):
		#服务真正所在主机信息
		self.host = host
		self.starttime = starttime
		self.stoptime = stoptime
		#要被截取的日志文件
		self.srcfile = srcfile
		#截取后生成的新文件,我们要下载的日志文件 
		self.destfile = destfile
		#跳板机主机信息
		self.forwarding_host= forwarding_host
		self.conport = conport
		self.linenum = linenum
	def abc(self):
		return self.host
		
	#返回多少分钟之前的时间戳
	def Unixminutespar(coutt):
		listaa = ((datetime.datetime.now()-datetime.timedelta(minutes=coutt)).strftime("%Y %m %d %H %M %S"))
		nian, yue, ri, shi, fen, miao = listaa.split(" ")
		dateC = datetime.datetime(int(nian), int(yue), int(ri), int(shi), int(fen),0)
		timestamp=time.mktime(dateC.timetuple())
		return str(timestamp)[:-3]
	#返回多少分钟之前的时间
	def minutespar(coutt):
		return ((datetime.datetime.now()-datetime.timedelta(minutes=coutt)).strftime("%Y-%m-%d %H:%M"))
	def progress_bar(self, transferred, toBeTransferred, suffix=''):
		# print "Transferred: {0}\tOut of: {1}".format(transferred, toBeTransferred)
		print "\n"
		bar_len = 60
		filled_len = int(round(bar_len * transferred/float(toBeTransferred))) 
		percents = round(100.0 * transferred/float(toBeTransferred), 1)
		bar = '=' * filled_len + '-' * (bar_len - filled_len)
		sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
		sys.stdout.flush()
		
	def isFile(self, Listdir, filename):
		isfile = 0
		for rt, dirs, files in os.walk(Listdir):
			for file in files:
				if file == filename:
					isfile = 1
					#print "有同名"
					break
		return isfile
	
	def remote_scp(self):
		if self.forwarding_host != None:
			self.host = self.forwarding_host
		t = paramiko.Transport((self.host["ip"],self.host["port"]))  
		t.connect(username=self.host["user"], password=self.host["pswd"])  # 登录远程服务器   
		sftp = paramiko.SFTPClient.from_transport(t)   # sftp传输协议  
		src = self.destfile + '.gz'   
		#下载前，查看当前目录是否有同名文件，如有在文件名前面加（1）,加过（1）再判断，如还有同名，自增为(2)....
		i = 0
		dess = src
		upload = os.path.normpath(os.path.abspath(".") + "/upload/")
		while True:
			i += 1
			if self.isFile(upload, dess) == 1:
				dess = '(' + str(i) + ')' + src
				print dess
				continue
			break
		#os.path.normcase(path)在Linux下，该函数会原样返回path，
		#					   在windows平台上会将路径中所有字符转换
		#des = os.path.normcase(os.getcwd() + "/") + local_path
		des = upload + os.sep + dess
		print u"已下载到%s" % des
		sftp.get(src,des,callback=self.progress_bar)  
		t.close() 
		return dess

	def getdockerinfo(self):
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(self.host['ip'], int(self.host['port']), self.host['user'], self.host['pswd'], timeout=5)
		cmda = 'docker info | grep \"Root Dir\" | awk \'{print $3}\''
		print cmda
		stdin, stdout, stderr = ssh.exec_command(cmda)
		wocao = stdout.read().strip('\n')
		ssh.close()
		return wocao
		
	def ssh_download(self):
			# host = {
				# 'ip':'12.22.33.44',
				# 'port':22,
				# 'user':'root',
				# 'pswd':'passwd'
			# }
		#需要跳板操作直接换函数
		if self.forwarding_host != None:
			return self.Forwarding()
		try:
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(self.host['ip'], int(self.host['port']), self.host['user'], self.host['pswd'], timeout=5)
			
			#端口号是否有值，为判断是否在容器里
			if self.conport != None:
				#获取完整容器ID
				cmda = 'docker ps --no-trunc=true | grep :' + str(self.conport) + '- | awk \'{print $1}\''
				print cmda
				stdin, stdout, stderr = ssh.exec_command(cmda)
				#print cmd
				conID = stdout.read().strip('\n')
				#操作文件名 （绝对路径)
				dockerdiff = self.getdockerinfo()
				SrcFilePath = dockerdiff + '/diff/' + conID + self.srcfile 
			else:
				SrcFilePath = self.srcfile
			DestFilePath = '/root/' + self.destfile
			
			#短连接服务日期格式为2016-08-19 10:10:01
			#拼接截取命令
			if self.linenum:
				cmdb = 'tail -n ' + self.linenum + ' ' +  SrcFilePath + ' > ' + DestFilePath
			else:
				cmdb = 'sed -n \'/' + self.starttime + '/,/' + self.stoptime + '/p\' ' + SrcFilePath +' > ' + DestFilePath
			print cmdb
			stdin, stdout, stderr = ssh.exec_command(cmdb)
			#如有服务器返回错误，则判定此次操作失败
			if stderr.readlines():
				print u"远程执行截取操作失败。服务器故障02:%s" % stderr.read()
				print u"readlines: %s" % stderr.readlines()
				return u"远程执行截取操作失败。服务器故障02:%s" % stderr.readlines()
				#抛出  SystemExit异常 
				#sys.exit()
				
			#如果文件大小为零，给于提示
			cmdc = 'du ' + DestFilePath + ' | awk \'{print $1}\''
			stdin, stdout, stderr = ssh.exec_command(cmdc)
			FileSize = stdout.read().strip('\n')
			if FileSize == "0":
				print u"提示：文件大小为零！！！错误03"
				return u"提示：文件大小为零！！！错误03"
			# 压缩文件 
			cmde = 'gzip ' + DestFilePath
			stdin, stdout, stderr = ssh.exec_command(cmde)
			if stderr.readlines():
				print u"远程执行压缩操作失败。服务器故障04: %s" % stderr.readlines()
				return u"远程执行压缩操作失败。服务器故障04: %s" % stderr.readlines()
				#抛出  SystemExit异常
				#sys.exit()
				
			#下载日志文件
			#返回新文件名，
			dest = self.remote_scp()
			
			#删除临时文件
			stdin,stdout,stderr = ssh.exec_command('rm -rf ' + DestFilePath + ' && rm -rf ' + DestFilePath + '.gz')
			if stderr.readlines():
				print u"远程执行删除临时文件操作失败。服务器故障05: %s" % stderr.readlines()
				return u"远程执行删除临时文件操作失败。服务器故障05: %s" % stderr.readlines()
				#sys.exit()
			return dest
		finally:
			ssh.close()
			
			
	def Forwarding(self):

		try:
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(self.forwarding_host['ip'], int(self.forwarding_host['port']), self.forwarding_host['user'], self.forwarding_host['pswd'], timeout=5)
			print u"开始执行..."
			
			#拼接配置中心启动隧道中转脚本命令
			#接入服务docker的宿主机需要配置中心服务器跳转，所以所有操作需要放到配置中心
			if self.conport != None:
				cmd = 'python /root/tools/SplitLog.py \"' + str(self.host) + '\" "' + self.starttime + '" "' + self.stoptime + '" "' + self.srcfile + '" "' + self.destfile + '" "' + str(self.conport) + '"'
			else:
				cmd = 'python /root/tools/SplitLog.py \"' + str(self.host) + '\" "' + self.starttime + '" "' + self.stoptime + '" "' + self.srcfile + '" "' + self.destfile + '"'

			stdin, stdout, stderr = ssh.exec_command(cmd)
			# reload(sys)
			# sys.setdefaultencoding('utf-8')
			# for out in stdout.readlines():
				# print u"out:%s" % out.encode('gb2312')
			for err in stderr.readlines():
				print 	u"err:%s" % err
			if stderr.readlines():
				print u"启动命令失败,001"
				return u"启动命令失败,001"
			# 这个OK会在配置中心脚本中，以最后完成所有操作打印输出 
			elif stdout.readline().strip('\n') == 'OK':
				print u"隧道执行成功。开始下载到本地..."
				
			#从配置中心服务器下载到本地
			SrcFile = self.destfile + '.gz'
			dest = self.remote_scp()
			
			#删除临时文件
			stdin,stdout,stderr = ssh.exec_command('rm -rf ' + SrcFile)
			if stderr.readlines():
				print u"远程执行删除临时文件操作失败。服务器故障05: %s" % stderr.readlines()
				return u"远程执行删除临时文件操作失败。服务器故障05: %s" % stderr.readlines()
			else:
				#操作成功
				return dest
		finally:
			ssh.close()
		