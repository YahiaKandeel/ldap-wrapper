#!/usr/bin/python
import ldap_wrapper as ldap

# Connecting to LDAP
ad = ldap.LDAP(user=ldap.user, password=ldap.password,
               server=ldap.server, base=ldap.base, page_size=ldap.page_size)
ad.connect()

# result
output = 'data/users.csv'

# Dumping all AD
data = ad.dump_all()
users = data['users']

# Decoding all users
decoded_users = {}

for cn in users:
    decoded_users[cn] = ldap.userdecode(users[cn])
    decoded_users[cn]['ou'] = ','.join((cn.split(',')[1:]))

# keys
keys = [	'sAMAccountName', 'displayName', 'ou', 'userAccountControl', 'mail', 'proxyAddresses', 'description', 'manager', 'employeeID', 'employeeStatus',
         'company', 'department', 'directReports', 'directorate', 'ipPhone', 'employeeMobile', 'memberOf', 'msRTCSIP-UserEnabled', 'title', 'c', 'co', 'l',
         'whenCreated', 'lastLogonTimestamp', 'pwdLastSet', 'accountExpires', 'badPasswordTime', 'badPwdCount', 'lastLogoff', 'lastLogon', 'logonCount',
                        'homeDirectory', 'homeDrive']


# Write it down
ldap.misc.save_data_to_csv_file(
    output, decoded_users, keys, ',', ' # ', replace_bad=';')

# Notify
ldap.misc.notify(output, 'eng.qandeel@gmail.com', 'ALL Users')
