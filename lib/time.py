#!/usr/bin/python
########################################################################
##### LDAP time converter 
########################################################################
import datetime
import sys

def ldap_time_converter(timestamp):
	'''Time Convert Function'''

	try:
		#### Convert YMD LDAP timestamps
		if '0z' in timestamp.lower():
			converted_time = datetime.datetime.strptime(timestamp, "%Y%m%d%H%M%S.0z")
			converted_time = str(converted_time.date())
		
		#### Convert 18-digit LDAP timestamps to human readable date
		else:
			#### Ignore millisecond
			timestamp = timestamp[:18]
			#### epoch Time
			epoch_start = datetime.datetime(year=1601, month=1,day=1)
			#### Timestamp to Seconds since epoch 
			seconds_since_epoch = float(timestamp)/10**7
			#### Convert Timestamp
			converted_time = epoch_start + datetime.timedelta(seconds=seconds_since_epoch)
			#### Convert it to day
			converted_time = str(converted_time.date())

	except:
		print >> sys.stderr, "timestamp Error", timestamp
		converted_time = str(timestamp)
	
	return converted_time