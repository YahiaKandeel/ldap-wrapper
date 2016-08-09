# ldap-wrapper

Configure conf/ldap.conf with the right parameters..

Please note that, all searches are case insensitive 

## Import 
```
from ldap_wrapper import LDAP, UserDecoder, search
```

##Connect to LDAP:
```
ad = LDAP()
ad.connect()
```

## Dumping all Users
you can dump users, groups, contacts and computers as well
```
users = ad.dump_users()
groups = ad.dump_groups()
data = ad.dump_all()
```

## Search
You have two options, online search that binds to LDAP and search against it, or offline search, that searches against the dumped data.

### Online Search in AD
You have only two methods for the current verion, search_by_sam and search_by_name, those methods supports wildcards.
```
match = ad.search_by_sam('kandi*')
match = ad.search_by_name('yahia*')
```

### Offline Search in AD
Offline search is based on regex... 
You have only search method, this method takes five parameters 
* The dumpped data(users, groups, coputers..etc)
* SAM --> for sam search
* Name --> for DisplayName search
* keyName --> if you have another criteria you need to search against, name it here
* keyValue --> comes with keyName, and it should contains the value here
```
# search all users that have kandi in their SAM
match = search(users, sam='kandi')
# search all groups named as '*security*'
matched_groups = search(groups, name='seacurity')
# search all users that their manager '*yahia*'
match = search(users, keyName='manager', keyValue='yahia')
```

## Decoding
The Current version supports only user decoder, you can decode the users by creating an object from UserDecoder, then call decode method.
```
for cn in match:
 	 print UserDecoder(match[cn]).decode()
```
