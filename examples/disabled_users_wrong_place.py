#!/usr/bin/python
from ldap_wrapper import LDAP, separator

#### Connecting and Dumping all AD
ad = LDAP()
ad.connect()

users = ad.dump_users()

#### Decoding all users
decoded_users = {}
for cn in users:
	user =  UserDecoder(users[cn]).decode()
	if 'Disabled' in user['userAccountControl'] and 'disable' not in cn.lower():
		decoded_users[cn] = user
		decoded_users[cn]['ou'] = ','.join((cn.split(',')[1:]))

#### Generating TXT
keys = [	'sAMAccountName', 'displayName' ,'ou', 'userAccountControl', 'mail', 'proxyAddresses', 'description', 'manager', 'objectClass',
			'company',  'whenCreated' , 'lastLogonTimestamp' ,  'pwdLastSet', 'accountExpires', 
			'homeDirectory']

txt = convert_hash_to_text(decoded_users, keys, separator)

#### Writing it down
open('data/disabled_users_wrong_place.csv','w').write(txt)