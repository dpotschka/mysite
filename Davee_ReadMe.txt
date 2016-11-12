DAvee Read these for setting up your website connections etc.

All the stuff in the file is from the tutorial:
https://docs.djangoproject.com/en/1.10/intro/tutorial01/


1.

Always make sure your virtualenv is active when working on the
django tutorial.  If you need to reactivate it later, maybe if
you close your bash console and open a new one, the command is:

workon django17
--


Set up your directory structures the same way as done in this example web site
(mysite).
Django is set up to search all apps in one web site (mysite).  A website can
have more than one app.

You need to nest your templates down so that Django doesn't grab templates
from one of your other apps.

like you have here:
/mysite/myPolls/templates/myPolls/index.html

mysite is your website and myPolls is an application in that website.

--


To format the html of your admin page

You have two template directories one is for admin.py and is found at:
https://www.pythonanywhere.com/user/timetable/files/home/timetable/mysite
   /templates/admin
I also had to create that admin directory.  According to the tutorial.

You also have two admin directories,
the second one is for static files and is in:
/mysite/myPolls/static/admin

In lesson 7 of the tutorial when you get to this part:
"Now create a directory called admin inside templates, and
copy the template admin/base_site.html from within the
default Django admin template directory in the source code
"of Django itself (django/contrib/admin/templates) into that directory.

You must enter this url to get that file:
https://www.pythonanywhere.com/user/timetable/files/usr/local/lib/python2.7/dist-packages/django/contrib/admin/templates/admin

I got it here already:
<!--
{% extends "admin/base.html" %} {% block title %}
{{ title }} | {{ site_title|default:_('Daves site admin') }}{% endblock %}

{% block branding %}
{{ site_header|default:_('Daves administration') }}

{% endblock %} {% block nav-global %}{% endblock %}
-->

change it to this:

{% extends "admin/base.html" %}
{% block title %}{{ title }} | {{ site_title|default:_('Daves site admin') }}
{% endblock %}

{% block branding %}
Dave is a cool administrator

{% endblock %} {% block nav-global %}{% endblock %}


then,

Set
mysite/settings.py
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [os.path.join(BASE_DIR, 'templates')],...


-- End To Format the html of your admin page


We'll discuss in more detail in the reusable apps tutorial why we do this
multiple template and admin directories.
https://docs.djangoproject.com/en/1.10/intro/reusable-apps/





---- End 1



2.

This is found on the very front of pythonAnywhere and is the first pointer
to your web site files.  Set it up to do that.
/var/www/timetable_pythonanywhere_com_wsgi.py

---- End 2


3.

To log into the virtual environment for Django type <workon django17>.
When using the bash console don't forget to cd mysite.
type <python manage.py shell>, to get ipython integrated developer shell.
type exit() to exit either of the above two, they are independant you can't
be in both at the same time unles you open up two shells.

---- End 3


4.

In:
/timetable/mysite/manage.py

set
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")


---- End 4


5.

In:
/timetable/mysite/mysite/settings.py

set
ALLOWED_HOSTS = ["timetable.pythonanywhere.com"]

and watch out for this:

# Application definition

INSTALLED_APPS = [

    # Watch out for this I think it was autogenerated, should be
    # a cap P here  |  I worked a fix for it though.
    'myPolls.apps.MypollsConfig',

--

set
ROOT_URLCONF = 'mysite.urls'

set
WSGI_APPLICATION = 'mysite.wsgi.application'


If you want to use a different db, I believe you set it here:

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/  #databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

--

set
TIME_ZONE = 'America/Vancouver'


This is already set for you:
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'


---- End 5


6.

In:
/timetable/mysite/mysite/urls.py

That is your first url mapper and points to the handlers and
additional url mappers.
Goto that file for more detailed help.


---- End 6



7.

In:
/timetable/mysite/mysite/wsgi.py

That is your second wsgi pointer (see 2 above).

set
path = '/home/timetable/mysite'

set
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")


---- End 7



8.


In:
/timetable/mysite/myPolls/admin.py

Register you db models here.


---- End 8


9.

In:
/timetable/mysite/myPolls/apps.py

# Watch out for this, I think it was autogenerated, should be a cap P
# here  |
class MypollsConfig(AppConfig):
    name = 'myPolls'


---- End 9


10.

In:
/timetable/mysite/myPolls/models.py

This is where you declare your class db models.

---- End 10


11.

In:
/timetable/mysite/myPolls/tests.py

Django will look here for testing from bash.  Write your own tests
there are some in here we did for the mysite project.
See the tutorial on how to access these tests from bash.
https://docs.djangoproject.com/en/1.10/intro/tutorial05/


---- End 11



12.

In:
/timetable/mysite/myPolls/urls.py

That is your second url mapper (see 6 above).


# This tells django which app the urls belong to
# when using the url tag var in an html file, see
# templates/myPolls/index.html.  It is very important to set this.
See the bottom of tutorial 3:
https://docs.djangoproject.com/en/1.10/intro/tutorial03/

Hit ctrl F in chrome to search for a string.

set
app_name = 'myPolls'


---- End 12



13.

In:
/timetable/mysite/myPolls/views.py

This is where all your handlers reside.
Very cool, visit it and learn the way Django does stuff.


---- End 13



14.

In
/mysite/myPolls/templates/myPolls

That is where your html files are and
NOTE how the final "myPolls" directory is nested down after templates,
Django will search all apps with a templates folder and it will pick
the first html file after that templates folder

that matches your path/name.html so if you have more than
one app running on the same web site (ie you will have more than
one templates folder) you BETTER MAKE DAM SURE YOU
NEST YOUR FINAL DIRECTORY AFTER THE templates directory!!!
Do NOT store html files like this /templates/name.html


The same goes for static files (css, javascript):

Static file namespacing

Just like templates, we might be able to get away with putting our
static files directly in myPolls/static (rather than creating another
MyPolls subdirectory), but it would actually be a bad idea.
Django will choose the first static file it finds whose name

matches, and if you had a static file with the same name
in a different application, Django would be unable to distinguish
between them. We need to be able to point Django at the
right one, and the easiest way to ensure this is by namespacing

them. That is, by putting those static files inside another directory
named for the application itself.

---- End 14


15.

Make your life easy and use the virtual environment (with the console bash)
and the turorial to auto set up most of the stuff for you.

These two tutorials work together.  PythonAnywhere is a bit different
from developing locally so you must follow both tutorials at the same time.

pythonAnywhere Django docs.
https://help.pythonanywhere.com/pages/FollowingTheDjangoTutorial

Official Django website docs.
https://docs.djangoproject.com/en/1.10/intro/tutorial01/



---- End 15



16.


How to setup static files in Django
There are 3 main things to do:

set STATIC_ROOT in settings.py
run manage.py collectstatic
set up a Static Files entry on the PythonAnywhere Web tab.
Optionally, you can also customise STATIC_URL, if you want to
use a static URL prefix other than /static/

Set STATIC_ROOT in settings.py

The STATIC_ROOT variable in settings.py defines the single folder
you want to collect all your static files into. Typically, this
would be a top-level folder inside your project, eg:

STATIC_ROOT = "/home/myusername/myproject/static"
# or, eg,
STATIC_ROOT = os.path.join(BASE_DIR, "static")
The important thing is this needs to be the full, absolute path
to your static files folder.

From bash virtual environment shell (see 3 above)
Run manage.py collectstatic

This command collects up all your static files from each of
your app folders (including the static files for the admin app)
and from any other folders you specify in settings.py, and copies
them into STATIC_ROOT.

You need to re-run this command whenever you want to publish new
versions of your static files.

(Optionally) change STATIC_URL

If you really must, you can change the default STATIC_URL,
which is /static/, to being a different prefix, like /assets/, or whatever
it may be. You'll probably want to use the {% static %} template
tag with this in your html file. There's more info in the django docs.

Set up a static files mapping

Finally, set up a static files mapping to get our web servers
to serve out your static files for you.

Go to the Web tab on the PythonAnywhere dashboard
Go to the Static Files section
Enter the same URL as STATIC_URL in the url section (typically, /static/)
Enter the path from STATIC_ROOT into the path section (the full
path, including /home/username/etc)
Then hit Reload and test your static file mapping by going to
retrieve a known static file.

Eg, if you have a file at /home/myusername/myproject/static/css/base.css,
go visit http://www.your-domain.com/static/css/base.css
or just run your web page with some pretty colors.

Serving static files in development

Django does have an alternative for serving static files during
development, which can avoid the need for you to run collectstatic
whenever you make changes to your files, but it comes at the cost of
putting an extra processing burden on the Python parts of your app.
If you really want to use this, you'll find more info in the django docs.

Media files

If you're using Django's default uploaded files handling, then
you'll need to set up a similar static files mapping from MEDIA_URL
to MEDIA_ROOT...

--

Warning

I think this refers to using command:
python manage.py collectstatic


Of course the {% static %} template tag is not available for use
in static files like your stylesheet which aren’t generated by
Django. You should always use relative paths to link your
static files between each other, because then you can
change STATIC_URL (used by the static template tag to
generate its URLs) without having to modify a bunch of
paths in your static files as well.


---- End 16


17.

Git stuff.


To get your PA files on your local machine you have to push them to
github first (use PA bash),  You may have to pull the github files
to PA first to integrate the two repos.

https://github.com/dpotschka/mysite

then you can pull them from github to your local directory using
your local bash.
cd into your local directory first.

Me on github:
https://github.com/dpotschka/mysite

Me on pythonAnyWhere:
https://www.pythonanywhere.com/user/timetable/files/home/timetable/mysite

Me on my local machine:
c:/Daves_Python_Programs/pythonAnyWhere/mysite.

--


Type help to get help with commands.

To initialize a new repository (repo):
goto the directory where you want the repo to be.
git init

Get repository (repo) setup here and a lot more:
http://www.njedesign.com/github-basic-commands-for-creating-and-pushing-to-repository/

to add files:
git add mysite/
then
git commit
To exit a message while doing a "git commit":
hit <esc>
then
:wq and the commit will happen.

More useful commands:
Use the https if you don't have ssh,
free accounts don't have ssh.

git clone <repo URL from GitHub>
cd into the newly-cloned directory.
git diff
git push
git pull

for debugging
git branch -a
and
git log



--------------------------- End 17 Git stuff




