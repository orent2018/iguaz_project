#!/usr/bin/python
# **********************************************
#
#  name:    install.py
#
#  purpose: Use a json based configuration file to install a group of servers
#           by populating an ansible configuration file and running a playbook
#           which based on the variables configure the servers in the list
#
#  parameters: The config file will contain a list of the servers and packages to be deployed
#
#  Output:     The intermediate result is the ansible variable yaml that will be used by the
#              ansible playbook for installing the servers
#
#  Created: 09/10/2018
#
#  Maintainer: Oren Teomi
#
# **********************************************
import os
import sys
import json

config_file="config.json"
inventory_file="/etc/ansible/hosts"
ansible_var_file="ansible/variables.yml"

# Functions
# *********
def populate_variables(var_group):
    for key,val in config[var_group].items():
      ansible_var.write(key+': '+val+'\n')
   
# import the config data from the config file to a dictionary object
# ****************************************************************
try:
  with open(config_file,'r') as cf:
    config=json.load(cf)
except IOError as e:
    print 'Error:The required file [',config_file,'] does not exist!!'
    sys.exit()

# *****************************************************************

# Add host list to host file
# **************************
if len(config['app_servers']):
  try:
    with open(inventory_file,'a') as inv_f:
       inv_f.write('[app_servers]\n')
       for server in config['app_servers']:
         inv_f.write(server+'\n')
  except IOError as e:
    print 'Error: Cannot access inventory file [',inventory_file,']!!'
    sys.exit()
else:
   print 'No target servers found - can not continue!!'
   sys.exit()

# Add Yum packages to ansible variables file
# *****************************************
if len(config['yum_packages']):     # Make sure yum package list is not empty
  with open(ansible_var_file,'w') as ansible_var:
     ansible_var.write('---\n'+'yum_packages:\n')
     for yum_pkg in config['yum_packages']:
       ansible_var.write(' - '+yum_pkg+'\n')

# Add Python packages to ansible variables file
# *********************************************
if len(config['python_packages']):   # Make sure python package list in not empty
  with open(ansible_var_file,'a') as ansible_var:
     ansible_var.write('python_packages:\n')
     for py_pkg,version in config['python_packages'].items():
        if version:
           ansible_var.write(' - { name: '+py_pkg+',version: '+version+' }\n')
        else:
           ansible_var.write(' - '+py_pkg+'\n')

# Add Files to copy to ansible variables file
# *******************************************
if len(config['files']):             # Make sure that file list is not empty
  with open(ansible_var_file,'a') as ansible_var:
     ansible_var.write('files:\n')
     for file in config['files']:
       ansible_var.write(' - '+file+'\n')

# Add key values including user,go and shellz to ansible variables file
# *********************************************************************
  with open(ansible_var_file,'a') as ansible_var:
    populate_variables('user_params')
    populate_variables('go_params')
    populate_variables('shellz_params')

# Run the ansible playbook
# ************************
os.system("ansible-playbook ansible/main.yml")

##################################################
