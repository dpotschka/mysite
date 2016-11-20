"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os
import sys

# For local.
path = 'C:/Daves_Python_Programs/pythonAnyWhere/mysite'

# For production on pa.
#path = '/home/timetable/mysite'

if path not in sys.path:
    sys.path.append(path)

from django.core.wsgi import get_wsgi_application

# Davee Tutorial has this.
# os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
# In the tutorial help from pythonAnywere
# about half way through where you see this:

#Go to the Virtualenv section and enter the path to your
#virtualenv, something like this: /home/myusername/.virtualenvs/django17
#Then, find the link to edit your wsgi file, scroll
#through it, and uncomment the parts that pertain to
#django -- something like this...

# I think they mean this file which is found on the front
# page of pythonAnywhere.com:  so I changed it.
#https://www.pythonanywhere.com/user/timetable/files/var/www/
# timetable_pythonanywhere_com_wsgi.py?edit


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

application = get_wsgi_application()
