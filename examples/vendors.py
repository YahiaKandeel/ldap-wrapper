#!/usr/bin/python
import ldap_wrapper as ldap

#### Connecting to LDAP
ad = ldap.LDAP(user=ldap.user, password=ldap.password, server=ldap.server, base=ldap.base, page_size=ldap.page_size)
ad.connect()

#### Dumping all AD users
users = ad.dump_users()

#### Output

output = 'data/vendors.csv'

#### Get All Users Which are member of VendorSupport
vendors = ldap.search(users, Key='memberOf', Value='VENDORSUPPORT')

#### Decoding all users
decoded_users = {}
for cn in vendors:
	decoded_users[cn] = ldap.userdecode(vendors[cn])
	decoded_users[cn]['ou'] = ','.join((cn.split(',')[1:]))

#### Generating TXT
keys = [	'sAMAccountName', 'displayName' ,'ou', 'userAccountControl', 'mail', 'proxyAddresses', 'description', 'manager', 'employeeID', 'employeeStatus', 
			'company' , 'department', 'directReports', 'directorate', 'ipPhone', 'employeeMobile', 'memberOf', 'msRTCSIP-UserEnabled', 'title', 'c', 'co', 'l',
			'whenCreated' , 'lastLogonTimestamp',  'pwdLastSet', 'accountExpires', 'badPasswordTime', 'badPwdCount', 'lastLogoff', 'lastLogon', 'logonCount',
			'homeDirectory', 'homeDrive' ]

####
ldap.misc.save_data_to_csv_file(output, decoded_users, keys , ',' , ' # ', replace_bad=';')

#### Notify 
ldap.misc.notify(output, 'eng.qandeel@gmail.com', 'Vendor Support Users')
