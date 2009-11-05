#!/usr/bin/env python

import sys
import re

log_line_re = re.compile(r'''(?P<remote_host>\S+) #IP Address
				\s+ #white space
				\S+ #remote logname
				\s+ #white space
				\S+ #remote user
				\s+ #whitespace
				#\[[^\[\]+\] #time
				\[.*\]
				\s+ #whitespace
				"[^"]+" #first line of request
				\s+ #whitespace
				(?P<status>\d+) 	
				\s+ #whitespace
				(?P<bytes_sent>-|\d+)
				\s* #whitespace
				''', re.VERBOSE)

def check_args():
	if len(sys.argv) != 2:
		print "Error sys.argv[0]: <LogFile>"
		sys.exit(1)

def dictify_logline(line):
	'''return a dictionary of the the pieces we want from t apachone log file'''
	m = log_line_re.match(line)
	if m:
		groupdict = m.groupdict()
		if groupdict['bytes_sent'] == '-':
			groupdict['bytes_sent']  = '0'
		return groupdict
	else:
		return {'remote_host': None,
			'status' : None,
			'bytes_sent' : "0",
		}

def generate_log_report(logfile):
	'''Return dict of format remote_host => [list of bytes sent]
	Function takes an apache file object '''
	report_dict = {}
	for line in logfile:
		line_dict = dictify_logline(line)
		print line_dict
		try:
			bytes_sent = int(line_dict['bytes_sent'])
		except ValueError:
			#we dont know it fuck it
			continue
		report_dict.setdefault(line_dict['remote_host'], []).append(bytes_sent)
	return report_dict

if __name__ == '__main__':
	if not len(sys.argv) > 1:
		print "error sys.argv[0]: Need log file to parse"
		sys.exit(1)
	infile_name = sys.argv[1]
	try:
		infile = open(infile_name, 'r')
	except IOError:
		print "You must specify a valid file to parse"
		sys.exit(1)
	log_report = generate_log_report(infile)
	print log_report
	infile.close()
