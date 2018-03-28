#!/usr/bin/env bash

python server/donationcoordinator/manage.py makemigrations
python server/donationcoordinator/manage.py migrate
