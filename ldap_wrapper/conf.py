#!/usr/bin/python
########################################################################
# Config Reader
########################################################################
import ConfigParser, os

#### Getting abspath name
current_path = os.path.abspath(os.path.dirname(__file__))
#### Read Config
config = ConfigParser.ConfigParser()
config.read(os.path.join(current_path, "../conf/ldap.conf"))

#### seting Variables
server = config.get('server','server')
base =  config.get('server','base')
page_size = int(config.get('options','page_size'))

#### Styling
separator = config.get('style','separator') + ' '
sub_separator = config.get('style','sub_separator') + ' '

#### Cred
user = config.get('cred','user')
password = config.get('cred','password')