import os
import ConfigParser

# Getting BaseDir
baseDir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

# Read Config...
config = ConfigParser.ConfigParser()
config.read(baseDir + "/conf/mailer.conf")

# seting Variables
server = config.get('relay', 'server')
username = config.get('relay', 'username')
password = config.get('relay', 'password')

# Message
From = config.get('message', 'from')
