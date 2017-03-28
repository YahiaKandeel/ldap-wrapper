#!/usr/bin/python
########################################################################
# Decode All Needed LDAP parameters
########################################################################
import re
import functools
from time import ldap_time_converter

# User Account Control Mappings
user_account_control = {
    '512': 'Enabled',
    '514': 'Disabled',
    '544': 'Enabled & Password Not Required',
    '66048': 'Enabled & password never expires',
    '66050': 'Disabled & password never expires'
}


# Group Type Mapping
group_type = {
    '2': 'Global distribution group',
    '4': 'Domain local distribution group',
    '8': 'Universal distribution group',
    '-2147483646': 'Global security group',
    '-2147483644': 'Domain local security group',
    '-2147483640': 'Universal security group',
}

# User Attributes
user_attr = {
    # LDAP General Info
    'sAMAccountName': {},
    'cn': {},
    'memberOf': {},
    # Employee Info
    'title': {},
    'employeeID': {},
    'description': {},
    'employeeStatus': {},
    'company': {},
    'l': {},
    'c': {},
    'co': {},
    # Important Timings
    'whenCreated': {'func': ldap_time_converter},
    'pwdLastSet': {'func': ldap_time_converter},
    'lastLogonTimestamp': {'func': ldap_time_converter},
    'accountExpires': {'func': ldap_time_converter},
    'badPasswordTime': {'func': ldap_time_converter},
    'lastLogoff': {'func': ldap_time_converter},
    'lastLogon': {'func': ldap_time_converter},
    'badPwdCount': {},
    'logonCount': {},
    'userAccountControl': {'dict': user_account_control},
    # Other Info
    'department': {},
    'directorate': {},
    'employeeMobile': {},
    'ipPhone': {},
    'mobile': {},
    'homeDirectory': {},
    'homeDrive': {},
    'division': {},
    'displayName': {},
    'directReports': {},
    # Mails
    'msRTCSIP-UserEnabled': {},
    'mailNickname': {},
    'proxyAddresses': {'reg': 'smtp:([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,})'},
    'mail': {},
    # Hierarchy
    'objectClass': {},
    'manager': {'reg': 'CN=(\w[\s\w]*),OU='},
    'objectCategory': {},
}

# Group Attribures
group_attr = {
    # LDAP General Info
    'name': {},
    'sAMAccountName': {},
    'managedBy': {},
    'mail': {},
    'member': {},
    # Timing
    'whenCreated': {'func': ldap_time_converter},
    'whenChanged': {'func': ldap_time_converter},
    # Exchange Attributes
    'msExchRequireAuthToSendTo': {},
    'msExchRecipientDisplayType': {},
    # Group types
    'groupType': {'dict': group_type}
}


# Decode Function
def decode(item, attributes):
    result = {}

    for attr in attributes:
        dictionary = attributes[attr].get('dict')
        funcution = attributes[attr].get('func')
        regex = attributes[attr].get('reg')

        info = item.get(attr, '')

        if info:

            if funcution:
                if type(info) == list:
                    info = info[0]
                info = funcution(info)

            if dictionary:
                if type(info) == list:
                    info = info[0]
                info = dictionary.get(info, info)

            if regex:
                info = re.findall(regex, str(info), re.I)

        result[attr] = info

    return result


# User & Group Decoders
userdecode = functools.partial(decode, attributes=user_attr)
groupdecode = functools.partial(decode, attributes=group_attr)
