
  Server install automation
  *************************

  The main python code uses a json based configuration file to install a group of servers
  by populating an ansible configuration file and running a playbook
  which based on the variables configures the servers in the list.

  The playbook is divided into 3 subsections:

  1) The base installation of the yum,python packages and any files that need to be copied.

  2) The docker installer of the docker SW,service and bringing up of the Hello-World container

  3) The GO installer which installs go prepare the environment variables and then installs the shellz
     go project

   The config file will contain a list of the servers and packages to be deployed

   An intermediate result is the ansible variable.yml file that will be used by the
   ansible playbooks for installing the servers

   The installation is performed by running the python installer with a user with sudo priviledges as follows:

   sudo ./install.py

   packages and versions can be updated through the config.json input file.


   PREREQUISITES:

      - ansible version 2.5 and above
      - passwordless ssh into all servers in the app_servers server group
      - sudo priviledges for the user running the install script
      - The automation was tested on RHEL7 and may not work on CENTOS


  Created: 09/10/2018

  Maintainer: Oren Teomi

  EMAIL: orent66@gmail.com
