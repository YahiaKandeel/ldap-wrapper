#!/usr/bin/python
from ldap_wrapper import LDAP, UserDecoder, search, separator
from misc.helpers import convert_hash_to_text

#### Connecting to LDAP
ad = LDAP()
ad.connect()

#### Dumping all AD
users = ad.dump_users()

#### 
vendors = search(users,keyName='memberOf',keyValue='VENDORSUPPORT')

#### Decoding all users
decoded_users = {}
for cn in vendors:
	decoded_users[cn] = UserDecoder(vendors[cn]).decode()
	decoded_users[cn]['ou'] = ','.join((cn.split(',')[1:]))

#### Generating TXT
keys = [	'sAMAccountName', 'ou' , 'userAccountControl', 'mail', 'proxyAddresses', 'description', 'manager', 'objectClass',
			'company',  'whenCreated' , 'lastLogonTimestamp' ,  'pwdLastSet', 'accountExpires', 
			'homeDirectory']

txt = convert_hash_to_text(decoded_users, keys, separator)

#### Writing it down
open('data/ajn_vendors.csv','w').write(txt)

