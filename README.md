# ldap-wrapper

Configure conf/ldap.conf with the right parameters..

Please note that, all searches are case insensitive 

## Import 
```python
from ldap_wrapper import LDAP, UserDecoder, search
```

##Connect to LDAP:
```python
ad = LDAP()
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
# search(data, [sam='val'], [name='val'], [keyName='val'], [keyValue=val])
# data --> The dumpped data(users, groups, computers..etc)
# sam --> for sam search
# name --> for DisplayName search
# keyName --> if you have another criteria you need to search against, name it here
# keyValue --> comes with keyName, and it should contains the value here

# search all users that have kandi in their SAM
match = search(users, sam='kandi')

# search all groups named as '*security*'
matched_groups = search(groups, name='seacurity')

# search all users that their manager '*yahia*'
match = search(users, keyName='manager', keyValue='yahia')
```

## Decoding
The Current version supports only user decoder, you can decode the users by creating an object from UserDecoder, then call decode method.
```python
for cn in match:
 	 print UserDecoder(match[cn]).decode()
```

## Example
Suppose you want to dump all users in specific group, and convert the dumped data to csv and write it down..

```python
#!/usr/bin/python
from ldap_wrapper import LDAP, search
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

#### Generating csv
keys = [	'sAMAccountName', 'ou' , 'userAccountControl', 'mail', 'proxyAddresses', 'description', 'manager', 'objectClass',
			'company',  'whenCreated' , 'lastLogonTimestamp' ,  'pwdLastSet', 'accountExpires', 
			'homeDirectory']

csv = convert_hash_to_text(decoded_users, keys, separator)

#### Writing it down
open('data/ajn_vendors.csv','w').write(csv)
```
