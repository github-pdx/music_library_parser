#!/bin/bash
## Create a virtualenv, and activate:
sudo apt-get -y update
sudo apt-get -y install python3.9
sudo apt-get -y install build-essential libpq-dev libssl-dev gcc-multilib openssl libffi-dev zlib1g-dev
sudo apt-get -y install python3-pip python3-dev
sudo apt-get -y install python-virtualenv virtualenvwrapper
virtualenv -p /usr/bin/python3.9 venv
source venv/bin/activate
sudo -H pip3 install -r requirements.txt
