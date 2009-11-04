#!/usr/bin/env python
#
# parseVhost.py
# @author: 	kurtis velarde
# @email:	kurtisvelarde@gmail.com
# @date:		11/22/2009
#
# Takes http.conf file as stdin and retrieves the virtual host declarations
# example:
#	ssh localhost cat /etc/httpd/conf.d/* | python parseVhost.py
#
# Will be adding this to some sort of class but for now this works 


import sys
import re

#Declare Regex 
vhost_start = re.compile(r'<VirtualHost\s+(.*?)>')
vhost_end = re.compile(r'</VirtualHost>')
docroot_re = re.compile(r'(DocumentRoot\s+)(\S+)')
servername_re = re.compile(r'ServerName\s+(.*)')

def find_docroot(conf_string):
	'''find vhost from file type object'''
	in_vhost = False     #Check if we are in a virtual host directive 
	curr_vhost = None
	strVhost = ""
	newVhost = "*" * 50
	for line in conf_string:
		vhost_start_match = vhost_start.search(line)
		if vhost_start_match:
			curr_vhost = vhost_start_match.groups()[0]
			strVhost += "VirtualHost: " + curr_vhost + "\n"
			in_vhost = True
		if in_vhost:
			server_name = servername_re.search(line)
			if server_name:
				vservername = server_name.groups()[0]
				strVhost += "ServerName: " + vservername + "\n"
		if in_vhost:
			docroot_match = docroot_re.search(line)
			if docroot_match:
				vdocroot = docroot_match.groups()[1]
				strVhost += "DocumentRoot: " + vdocroot + "\n"
		vhost_end_match = vhost_end.search(line)
		if vhost_end_match:
			in_vhost = False
			print strVhost
			print newVhost
			strVhost = ""
		yield line

if __name__ == '__main__':
	'''do it'''
	config_string = sys.stdin.readlines()		#Get data from standard in
	for line in find_docroot(config_string):
		continue	
