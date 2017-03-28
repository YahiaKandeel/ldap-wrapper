# ldap-wrapper
The aim of this module to extract intersting data related to the users, groups, computers and contacts from your LDAP server, 

Configure: 
* conf/ldap.conf    for ldap parameter
* conf/mailer.conf  to support smtp notifications

Support:
* Dump users, groups, computers and contacts
* User & Groups Decode
* Convert extracted data to CSV
* Mail CSV file 'You can compress it as well'


Please note that, all searches are case insensitive 

## Import 
```python
from ldap_wrapper import ldap
```

##Connect to LDAP:
```python
### Create LDAP Instance
ad = ldap.LDAP(
				user = ldap.user, 
				password = ldap.password, 
				server = ldap.server, 
				base = ldap.base, 
				page_size = ldap.page_size
			)
### Connect					
ad.connect()
```

## Dumping all Users
you can dump users, groups, contacts and computers as well
```python
# Dump Users Only
users = ad.dump_users()

#Dump Groups Only
groups = ad.dump_groups()

# Dump Users, Computers, Contacts, Groups
data = ad.dump_all()

```

## Search
You have two options, online search that binds to LDAP and search against it, or offline search, that searches against the dumped data.

### Online Search in AD
You have only two methods for the current verion, search_by_sam and search_by_name, those methods supports wildcards.
```python
match = ad.search_by_sam('kandi*')
match = ad.search_by_name('yahia*')
```

### Offline Search in AD
Offline search is based on regex... 
```python
# Syntax:
# search(data, [sam='val'], [name='val'], [Key='val'], [Value=val])
# data --> The dumpped data(users, groups, computers..etc)
# sam --> for sam search
# name --> for DisplayName search
# Key --> if you have another criteria you need to search against, name it here
# Value --> comes with keyName, and it should contains the value here

# search all users that have kandi in their SAM
match = ldap.search(users, sam='kandi')

# search all groups named as '*security*'
matched_groups = ldap.search(groups, name='seacurity')

# search all users that their manager '*yahia*'
match = ldap.search(users, Name='manager', Value='yahia')
```

## Decoding
The Current version supports only user decoder, you can decode the users by creating an object from UserDecoder, then call decode method.
```python
decoded_users = {}
for cn in match:
 	 decoded_users[cn] = ldap.userdecode(users[cn])
```

## Example
Suppose you want to dump all users in specific group, and convert the dumped data to csv and write it down..

```python
#!/usr/bin/python
import ldap_wrapper as ldap

#### Create LDAP Instance
ad = ldap.LDAP(
				user = ldap.user, 
				password = ldap.password, 
				server = ldap.server, 
				base = ldap.base, 
				page_size = ldap.page_size
			)


#### Connecting to LDAP
ad.connect()

#### Dumping all AD
data  = ad.dump_all()
users = data['users']
### result
output = 'data/users.csv'

#### Dumping all AD
data  = ad.dump_all()
users = data['users']

#### Decoding all users
decoded_users = {}

for cn in users:
	decoded_users[cn] = ldap.userdecode(users[cn])
	decoded_users[cn]['ou'] = ','.join((cn.split(',')[1:]))

#### keys
keys = [	'sAMAccountName', 'displayName' ,'ou', 'userAccountControl', 'mail', 'proxyAddresses', 'description', 'manager', 'employeeID', 'employeeStatus', 
			'company' , 'department', 'directReports', 'directorate', 'ipPhone', 'employeeMobile', 'memberOf', 'msRTCSIP-UserEnabled', 'title', 'c', 'co', 'l',
			'whenCreated' , 'lastLogonTimestamp',  'pwdLastSet', 'accountExpires', 'badPasswordTime', 'badPwdCount', 'lastLogoff', 'lastLogon', 'logonCount',
			'homeDirectory', 'homeDrive' ]


#### Write it down
ldap.misc.save_data_to_csv_file(output, decoded_users, keys, ',' , ' # ', replace_bad=';')

#### Notify 
ldap.misc.notify(output, 'eng.qandeel@gmail.com', 'ALL Users')
```