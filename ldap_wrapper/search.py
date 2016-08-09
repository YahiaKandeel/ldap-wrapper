#!/usr/bin/python
############################
##### Offline LDAP Search
##### Works only if you have dumped all users & groups
##### Don't search on decoded data!!
############################
import sys, re
from conf import sub_separator

## Search in dumped data
def search(data, sam=False, name=False, keyName=False, keyValue=False):
	'''Generic search function to search on object by providing 
	a KeyName & KeyValue ...
	'''
	result = {}
	for cn in data:
		sAMAccountName = data[cn]['sAMAccountName'][0].lower()
		cn_name = re.findall('CN=(\w[\s\w]*)',cn)[0].lower()
		if sam:
			if re.findall(sam, sAMAccountName, re.I):result[cn] = data[cn]
		elif name:			
			if re.findall(name, cn_name, re.I):result[cn] = data[cn]
		elif keyName and keyValue:
			key = sub_separator.join(data[cn].get(keyName, 'N/A')).lower()
			if re.findall(keyValue, key, re.I):result[cn] = data[cn]
	return result