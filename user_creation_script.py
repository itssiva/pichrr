import os
import sys
#SCRIPT TO CREATE PROFILES, AFTER CREATING USERS
#FOR CREATING USERS UNCOMMENT THE CODE COMMENTRD AND VICEVERSA
os.environ['DJANGO_SETTINGS_MODULE'] = 'pichrr.settings'
import django


if __name__ == '__main__':
    django.setup()


# from post.models import Post
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from user_profile.models import UserProfile
print 'hello'
# print Post.objects.all()
usernames = ['theHulk', 'tonyStark', 'capt_America', 'Thor', 'blackWidow', 'hawkEye', 'loki', 'deadPool']
passwords = ['theHulk', 'tonyStark', 'capt_America', 'Thor', 'blackWidow', 'hawkEye', 'loki', 'deadPool']

for i in range(len(usernames)):

    email = usernames[i]+'@gmail.com'
    user = User.objects.create_user(username = usernames[i], password = passwords[i], email = email)
    user.save()
    email_address = EmailAddress(user=user,email=email, verified=True, primary=True)
    email_address.save()
