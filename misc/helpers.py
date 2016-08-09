#!/usr/bin/python
########################################################################
### Helper Functions
########################################################################
import re

########## Hash to Text Converter..
def convert_hash_to_text(data, keys, separator):
	'''Convert 2 level Hash to Text & putting in to consideration they provided keys'''
	txt = 'sep=' + separator + '\r\n' + separator.join(keys) + '\r\n'
	for d in data:
		for key in keys:
			value = str(data[d].get(key, ''))
			value = re.sub('[\r\n\;]', ' # ',value)
			txt += value + separator
		txt += '\r\n'
	return txt
