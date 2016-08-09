#!/usr/bin/python
from ldap_wrapper import *
from getpass import getpass

#### Connecting and Dumping all AD
ad = LDAP()
ad.connect()

groups = ad.dump_groups()

txt = 'sep=;\r\nCN; Type; SAM; Mail\r\n'
for cn in groups:
	group = groups[cn]
	auth_flag = group.get('msExchRequireAuthToSendTo', ['FALSE'])
	sam = group.get('sAMAccountName', ['None'])[0]
	mail = ', '.join(group.get('mail',['None']))
	groupType = group.get('groupType',['None'])[0]
	if auth_flag and auth_flag != ['FALSE']:
		txt += cn + '; ' + groupType + '; ' + sam + '; ' + mail + '\r\n'

open('data/groups_receives_mail_externally.csv','w').write(txt)