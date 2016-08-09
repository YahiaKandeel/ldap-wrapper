#!/usr/bin/python
from ldap_wrapper import LDAP, UserDecoder, search, separator, sub_separator

from misc.helpers import convert_hash_to_text

#### Connecting to LDAP
ad = LDAP()
ad.connect()

#### Dumping all AD
users = ad.dump_users()

users_with_multi_emails = {}
for cn in users:
	user = UserDecoder(users[cn]).decode()

	mails = set(user['mail'].lower().split(sub_separator))
	proxyAddresses = set(user['proxyAddresses'].lower().split(sub_separator))

	if len(mails) > 1 or len(proxyAddresses) > 1:
		users_with_multi_emails[cn] = {'sAMAccountName': user.get('sAMAccountName')}
		users_with_multi_emails[cn]['mails'] = sub_separator.join(mails)
		users_with_multi_emails[cn]['proxyAddresses'] = sub_separator.join(proxyAddresses)


csv = convertHashToText(users_with_multi_emails, ['sAMAccountName', 'mails', 'proxyAddresses'])
open('data/users_with_multi_emails.csv','w').write(txt)
