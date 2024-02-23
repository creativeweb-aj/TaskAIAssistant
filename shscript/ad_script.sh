#!/bin/bash
 cp /var/www/bewebe/shscript/.env  /var/www/bewebe/.env
 cp /var/www/bewebe/shscript/.env  /var/www/bewebe/src/.env
 sudo systemctl restart gunicorn