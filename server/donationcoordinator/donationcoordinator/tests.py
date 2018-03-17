from django.contrib.auth.models import User

def create_debug_users():
    User.objects.create_user("henryfbp", "henryfbp@gmail.com", "password")
    User.objects.create_user("root", "root@root.com", "root")
