#!/usr/bin/python
import ldap, sys, functools 
from conf import page_size, server, user, password, base
from ldap.controls import SimplePagedResultsControl

class LDAP():
	def __init__(self, server=server, user=user, password=password, base=base):
		self.server = server
		self.user = user
		self.password = password
		self.users = {}
		self.page_size = page_size
		self.base = base
		self.data = {'groups':{}, 'computers':{}, 'users':{}, 'contacts':{}}
	
	def __repr__(self):
		return "server: %s, user: %s, base: %s"%(self.server,self.user,self.base)
		
	def connect(self):
		try:
			self.ldapClient = ldap.open(self.server)
			self.ldapClient.simple_bind_s(self.user, self.password)
			self.ldapClient.set_option(ldap.OPT_REFERRALS, 0)
			self.ldapClient.protocol_version = 3
			print  >> sys.stderr, "Connected"
			self.password = None
			return True
		except:
			print  >> sys.stderr, "Not Connected"
		return False
	
	def search(self, filter, attributes=None):
		### Initialize Page Control
		self.pageControl = SimplePagedResultsControl(True, size= self.page_size, cookie='')
		### Initialize Filter
		searchFilter = filter #filters[filter]
		### Initialize Variables
		pages, result, first_pass = 0, [], True
		# Send search request First Time
		msgid = self.ldapClient.search_ext(self.base,ldap.SCOPE_SUBTREE, searchFilter, attributes,  serverctrls=[self.pageControl])
		# Pull the results from the search request
		while first_pass or self.pageControl.cookie:
			first_pass = False
			pages += 1
			print  >> sys.stderr, "Getting page %d" % (pages,)
			rtype, rdata, rmsgid, serverctrls = self.ldapClient.result3(msgid)
			print  >> sys.stderr, '%d results' % len(rdata)
			result.extend(rdata)
			### set page controls
			self.pageControl.cookie = serverctrls[0].cookie
			### Send search request Again
			msgid = self.ldapClient.search_ext(self.base, ldap.SCOPE_SUBTREE, searchFilter, attributes, serverctrls=[self.pageControl])
		# Convert Array to Hash
		result = dict(result)
		if result.has_key(None):del result[None]
		return dict(result)
	
	#dump all intersting Data from ad
	def dump_all(self):
		self.data['groups'] = self.search('(objectclass=group)')
		self.data['contacts'] = self.search('(objectclass=contact)')
		self.data['computers'] = self.search('(objectclass=computer)')
		users = self.search('(objectclass=user)')
		for cn in users:
			if cn not in self.data['computers'] and cn not in self.data['groups']:self.data['users'][cn] = users[cn]
		return self.data

	#search only users
	def dump_users(self) :return self.search(filter='(objectclass=user)')
	#search only groups
	def dump_groups(self):return self.search(filter='(objectclass=group)')

	# Search by SAM
	def search_by_sam(self, sAMAccountName):return self.search(filter='(sAMAccountName=%s)'%sAMAccountName)
	# Search by cn
	def search_by_name(self, cn):return self.search(filter='(CN=%s)'%cn)

	def close(self):
		self.ldapClient.unbind()