#!/usr/bin/python
import ldap_wrapper as ldap

### Connecting to LDAP
ad = ldap.LDAP(user=ldap.user, password=ldap.password, server=ldap.server, base=ldap.base, page_size=ldap.page_size)
ad.connect()

### result
output = 'data/groups_that_rcv_emails_externally.csv'

#### Dump Groups
groups = ad.dump_groups()

#### Decoding all groups
decoded_groups = {}

for cn in groups:
	decoded_groups[cn] = ldap.groupdecode(groups[cn])
	decoded_groups[cn]['cn'] = cn
	decoded_groups[cn]['len(Members)'] = len(decoded_groups[cn]['member'])


#### Assembling the output
keys = [  'cn', 'name' ,'groupType', 'sAMAccountName', 'mail', 'msExchRequireAuthToSendTo', 
		  'msExchRecipientDisplayType', 'len(Members)', 'managedBy', 'whenCreated', 'whenChanged']

####
ldap.misc.save_data_to_csv_file(output, decoded_groups, keys , ',' , ' # ', replace_bad=';')

####
ldap.misc.notify(output, 'eng.qandeel@gmail.com', 'Groups That Receives Mails Externally')
