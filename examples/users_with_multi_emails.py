#!/usr/bin/python
import ldap_wrapper as ldap

### Connecting to LDAP
ad = ldap.LDAP(user=ldap.user, password=ldap.password, server=ldap.server, base=ldap.base, page_size=ldap.page_size)
ad.connect()

#### Dumping all AD
data  = ad.dump_all()
users = data['users']

#### Decoding all users
users_with_multi_emails = {}

for cn in users:
	user           = ldap.userdecode(users[cn])
	mails          = list(set(user.get('mail')))
	proxyAddresses = list(set(user.get('proxyAddresses')))
	
	if len(mails) > 1 or len(proxyAddresses) > 1:
		users_with_multi_emails[cn] = {
										'sAMAccountName': user.get('sAMAccountName'),
										'mails': mails,
										'proxyAddresses':  proxyAddresses,
										}
###
keys = ['sAMAccountName', 'mails', 'proxyAddresses']

####
ldap.misc.save_data_to_csv_file('data/users_with_multi_emails.csv', users_with_multi_emails, keys , ',' , ' # ', replace_bad=';')
