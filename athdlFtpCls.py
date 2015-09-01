from ftplib import FTP
import re

#Current Release name format is athdl_linux_RHEL3_5.0_A1_110_19_2012
class AthdlFtpCls(object):
	def __init__(self,connectTo="www.athdl.com",year="2012"):
		self.connection = connectTo
		self.year = year
		self.latestRel = 0
		self.relCnt    = 0
		self.file = ""
		self.dir = []
		self.ftp1 = FTP(self.connection)
		self.ftp1.login("athdl","a1t9h9d9l")

	def _handleTransfer(self,block):
    		self.file.write(block)
    		print ".",
    

	def _findLatest(self,line):
    		match = re.match('.*athdl_linux_RHEL3_5.0_A1_(\d+)_19_2012.*', line)
    		if match:
			self.relCnt = self.relCnt + 1
			relNum = match.group(1)
			if (relNum > self.latestRel):
				self.latestRel = relNum 

	def _list(self,line):
		self.dir.append(line)

	def getLatest(self,getit):
		self.ftp1.cwd("RELEASES")
		self.ftp1.dir(self._findLatest)
		filename = 'athdl_linux_RHEL3_5.0_A1_%s_19_2012.tgz' % (self.latestRel)
		print "Latest File is ", filename
		if getit:
			self.file = open (filename,'wb')
			print "Getting ", filename
			self.ftp1.retrbinary('RETR ' + filename, self._handleTransfer)
		self.ftp1.cwd("..")
		
	def getList(self):
		self.ftp1.cwd("RELEASES")
		self.ftp1.dir(self._list)
		self.ftp1.cwd("..")
		return self.dir

	def getReleaseCnt(self):
		self.relCnt = 0
		self.ftp1.cwd("RELEASES")
		self.ftp1.dir(self._findLatest)
		self.ftp1.cwd("..")
		return self.relCnt

	def closeConnection(self):
		self.ftp1.close()

