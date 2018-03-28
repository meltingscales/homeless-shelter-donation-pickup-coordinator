release: python server/donationcoordinator/manage.py migrate
web: gunicorn --chdir server/donationcoordinator/ donationcoordinator.wsgi
