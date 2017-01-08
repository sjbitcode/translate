#!/bin/bash

sudo apt-get update

sudo apt-get -y upgrade

sudo apt-get install -y python3-pip
sudo apt-get install -y nginx
sudo apt-get install -y tree
sudo apt-get install -y git
sudo apt-get install -y libpq-dev postgresql postgresql-contrib

sudo mkdir -p /vagrant/logs/gunicorn
