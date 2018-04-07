#!/usr/bin/env bash

python server/donationcoordinator/manage.py makemigrations donator org 
python server/donationcoordinator/manage.py migrate
