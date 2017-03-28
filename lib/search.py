#!/usr/bin/python
########################################################
# Offline LDAP Search
# Works only if you have dumped all users & groups
# Don't search on decoded data!!
########################################################
import re

# Search in dumped data


def search(data, sam=False, name=False, Key=False, Value=False, sub_separator='\015'):
    '''Generic search function to search on object by providing 
    a KeyName & KeyValue ...
    '''
    result = {}

    for cn in data:

        # SAM Account Search
        if sam:
            sAMAccountName = data[cn]['sAMAccountName'][0]
            if re.findall(sam, sAMAccountName, re.I):
                result[cn] = data[cn]

        # Search By Name
        elif name:
            if re.findall(name, cn, re.I):
                result[cn] = data[cn]

        # Custom Search
        elif Key and Value:
            value = data[cn].get(Key)
            if re.findall(Value, str(value), re.I):
                result[cn] = data[cn]

    return result
