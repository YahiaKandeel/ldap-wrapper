#!/usr/bin/python
##################################################################
# Exporting Lib Modules...
# Parse ConfigFile
##################################################################
import os
import ConfigParser

# Getting BaseDir
baseDir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

# Read Config...
config = ConfigParser.ConfigParser()
config.read(baseDir + "/conf/ldap.conf")

# seting Variables
server = config.get('server', 'server')
base = config.get('server', 'base')
page_size = int(config.get('options', 'page_size'))

# Cred
user = config.get('cred', 'user')
password = config.get('cred', 'password')

# Styling
separator = config.get('style', 'separator')
sub_separator = '\015'
