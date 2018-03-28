#!/usr/bin/env bash

python server/donationcoordinator/manage.py makemigrations donationcoordinator donator org 
python server/donationcoordinator/manage.py migrate
