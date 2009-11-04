#!/usr/bin/env python
#
# vbconfig.py
#
# @author	Kurtis
#
#
# Horid quick way to add files vb sites :(
#

import optparse, sys,os
from confObject import ConfigFile, RunCon
import paramiko
#Main server configuration file
MASTER_CONF = 'server.conf'

#Main product file
MASTER_PRODUCT = 'product.conf'

#tmp file
TEMP_CONF = "tmp.conf"

def parse_opts():
	'''Parse options'''
	parser = optparse.OptionParser("Usage: %prog [options] arg1 arg2")
	
	parser.add_option('-S','--server', dest='server', default=None, type='string',
			help='Add a server name config file')
	parser.add_option('-I','--address', dest='ip', default=None, type='string',
			help='IP address for new server')
	parser.add_option('-F','--forum_root',dest='root', default=None, type='string',
			help='Forum root to install product')
	parser.add_option('-N','--name', dest='name', default=None, type='string',
			help='Name of added entry')

	parser.add_option('-P','--product', dest='product', default=None, type='string',
			help='Name of Product to install')
	parser.add_option('-U','--upload_root', dest='upload_root', default=None, type='string',
			help='The upload root on the local files system (must be readable)')
	parser.add_option('-R', '--run', dest='run', default=None, type='string',
			help='Run Console')

	(options, args) = parser.parse_args()

	if options.run:
		con = RunCon()
		server = con.get_args(MASTER_CONF)
		product = con.get_args(MASTER_PRODUCT)
		ip = server['ip']
		forum = server['forum_root'].strip()
		upload_root = product['upload_root'].strip()
		username = raw_input('Username: > ').strip()
		password = raw_input('Password: > ').strip()
		copyOver(upload_root, forum,username,ip, password)
		print forum
		print upload_root
	#make sure that only one action is taken
	if options.server and options.product:
		print 'error', sys.argv[0], ': Only can add one --product or --server entry at a time'
		sys.exit(-1)
	if options.server:
		if options.ip and options.root:
			try:
				d = { 'ip' : options.ip, 'forum_root' : options.root }
				newconfig = ConfigFile(MASTER_CONF,TEMP_CONF)
				newconfig.createEntry(options.server,d)
				newconfig.append_config()
			except:
				print "someting fucked"
		else:
			print 'Error:sys.argv[0]:'
	if options.product:
		if options.upload_root:
			try:
				d = { 'upload_root' : options.upload_root, 'product' : options.product}
				newconfig = ConfigFile(MASTER_PRODUCT,TEMP_CONF)
                                newconfig.createEntry(options.product,d)
				newconfig.append_config()
			except:
				"oppts"
		else:
			print "error:", sys.argv[0],"Must provide upload root when adding product"

                        master.close()
                        
def copyOver(mainDir, remoteDir, user, ip, password):
	'''simple recursive calling funtion'''
	if mainDir[len(mainDir)-1] != '/':
		mainDir += '/'
	file_list = os.listdir(mainDir)
	for f in file_list:
		res = f.find('.php')
		if res != -1:
			file_path = mainDir + f
			remote_path = remoteDir + "/" + f
			print 'trying to copy ', file_path, 'to', remote_path
			try:
				ssh = paramiko.SSHClient()
				ssh.set_missing_host_key_policy(
                                        paramiko.AutoAddPolicy())

				ssh.connect(ip,username=user.strip(),
                                        password=password.strip())
				ftp = ssh.open_sftp()
				ftp.put(file_path,remote_path)
				ftp.close()
			except:
				print "*ERROR*: file access isues dirctory not there etc..."
				continue
		elif os.path.isdir(mainDir + f):
			copyOver(mainDir + f, remoteDir + "/" + f, user,ip,password)


if __name__ == '__main__':
        parse_opts()

