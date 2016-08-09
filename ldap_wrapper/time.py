#!/usr/bin/python
########################################################################
##### LDAP time converter 
########################################################################
import re, datetime , sys

def timeConvert(timestamp):
	'''Time Convert Function'''
	try:
		#### Convert YMD LDAP timestamps
		if '0z' in timestamp.lower():
			converted_time = datetime.datetime.strptime(timestamp, "%Y%m%d%H%M%S.0z")
			converted_time = str(converted_time.date())
		else:
			#### Convert 18-digit LDAP timestamps to human readable date
			timestamp = timestamp[:18]
			epoch_start = datetime.datetime(year=1601, month=1,day=1)
			seconds_since_epoch = float(timestamp)/10**7
			converted_time = epoch_start + datetime.timedelta(seconds=seconds_since_epoch)
			converted_time = str(converted_time.date())
			# converted_time = datetime.datetime.fromtimestamp(float(timestamp)).strftime('%D')
	except:
		print >> sys.stderr, "timestamp Error", timestamp
		converted_time = 'None'
	return converted_time