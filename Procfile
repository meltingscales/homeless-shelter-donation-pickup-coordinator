release: chmod +x release-tasks.sh; ./release-tasks.sh
web: gunicorn --chdir server/donationcoordinator/ donationcoordinator.wsgi
delete-migrations: chmod +x remove-migrations.sh; ./remove-migrations.sh