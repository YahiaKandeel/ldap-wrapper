#!/usr/bin/python
from ldap_wrapper import LDAP, UserDecoder, separator
from misc.helpers import convert_hash_to_text

#### Connecting to LDAP
ad = LDAP()
ad.connect()

#### Dumping all AD
data = ad.dump_all()
users = data['users']

#### Decoding all users
decoded_users = {}
for cn in users:
	decoded_users[cn] = UserDecoder(users[cn]).decode()
	decoded_users[cn]['ou'] = ','.join((cn.split(',')[1:]))

#### Generating TXT
keys = [	'sAMAccountName', 'displayName' ,'ou', 'userAccountControl', 'mail', 'proxyAddresses', 'description', 'manager', 'objectClass',
			'company',  'whenCreated' , 'lastLogonTimestamp' ,  'pwdLastSet', 'accountExpires', 
			'homeDirectory']

txt = convert_hash_to_text(decoded_users, keys, separator)

#### Writing it down
open('data/ajn_users.csv','w').write(txt)
