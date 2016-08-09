#!/usr/bin/python
########################################################################
# Decode All Needed LDAP parameters 
########################################################################
import re, datetime , sys
from conf import sub_separator
from time import timeConvert

##### User Attributes
class UserDecoder():
	def __init__(self, user):
		self.user = user
		self.attributes = {	
						## LDAP General Info
						'sAMAccountName': 	{},
						'cn': 				{},
						'memberOf': 		{},
						## Employee Info
						'title': 			{},
						'employeeID': 		{},
						'description': 		{},
						'employeeStatus': 	{},
						'company': 			{},
						'l': 				{},
						## Important Timings
						'whenCreated': 			{'func': timeConvert},
						'pwdLastSet': 			{'func': timeConvert},
						'lastLogonTimestamp': 	{'func': timeConvert},
						'accountExpires': 		{'func': timeConvert},
						'userAccountControl': 	{'func': self.userAccountControl},
						## Other Info
						'department': 		{},
						'employeeMobile': 	{},
						'ipPhone': 			{},
						'mobile': 			{},
						'homeDirectory': 	{},
						'division': 		{},
						'displayName': 		{},
						## Mails
						'mailNickname': 	{},
						'proxyAddresses': 	{'reg': 'smtp:([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,})'},
						'mail': 			{},
						## Hierarchy
						'objectClass': 		{},
						'manager': 			{'reg': 'CN=(\w[\s\w]*),OU='},
						'objectCategory': 	{},
						}

		self.accountControl = {	'512': 'Enabled', '514': 'Disabled', 
							'544': 'Enabled & Password Not Required',
							'66048': 'Enabled & password never expires', 
							'66050': 'Disabled & password never expires'}

	def userAccountControl(self, code):
		return self.accountControl.get(code, code)

	##### User Decode ...
	def decode(self):
		result = {}
		for attr in self.attributes:
			func = self.attributes[attr].get('func')
			reg = self.attributes[attr].get('reg')
			info = sub_separator.join(self.user.get(attr,['None']))
			if func:info = func(info)
			if reg:info = sub_separator.join(re.findall(reg, info, re.I))
			result[attr] = info
		return result