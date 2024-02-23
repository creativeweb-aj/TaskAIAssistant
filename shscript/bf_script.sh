#!/bin/bash
rm -f /var/www/bewebe/.gitignore
rm -f /var/www/bewebe/requirements2.txt
rm -f /var/www/bewebe/appspec.yml
rm -f /var/www/bewebe/run.py
rm -f /var/www/bewebe/wsgi.py
rm -f /var/www/bewebe/.env
sudo chmod 777 -R  /var/www/bewebe
rm -rf /var/www/bewebe/src
rm -rf /var/www/bewebe/sql
rm -rf /var/www/bewebe/shscript
rm -rf /var/www/bewebe/beweplugin

