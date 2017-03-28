#!/usr/bin/python
import ldap_wrapper as ldap

### Connecting to LDAP
ad = ldap.LDAP(user=ldap.user, password=ldap.password, server=ldap.server, base=ldap.base, page_size=ldap.page_size)
ad.connect()

#### Dumping all AD
data  = ad.dump_all()
users = data['users']

### result
output = 'data/disabled_users_wrong_place.csv'

#### Decoding all users
decoded_users = {}

for cn in users:
	user = ldap.userdecode(users[cn])
	
	if 'Disabled' in user['userAccountControl'] and 'disable' not in cn.lower():
		decoded_users[cn] = user
		decoded_users[cn]['ou'] = ','.join((cn.split(',')[1:]))

#### Generating TXT
keys = [	'sAMAccountName', 'displayName' ,'ou', 'userAccountControl', 'mail', 'proxyAddresses', 'description', 'manager', 'objectClass',
			'company',  'whenCreated' , 'lastLogonTimestamp' ,  'pwdLastSet', 'accountExpires', 
			'homeDirectory']

#### Write it down
ldap.misc.save_data_to_csv_file(output, decoded_users, keys , ',' , ' # ', replace_bad=';')

#### Notify 
ldap.misc.notify(output, 'eng.qandeel@gmail.com', 'Disabled Users Wrong Place')
