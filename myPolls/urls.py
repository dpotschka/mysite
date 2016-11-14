from django.conf.urls import url

from . import views

# This tells django which app the urls belong to
# when using the url tag var in an html file, see templates/myPolls/index.html.
app_name = 'myPolls'


# Now we are going to use some generic views since many of our handlers
# were similar.  See the end of lesson 4 at:
# https://docs.djangoproject.com/en/1.10/intro/tutorial04/
# The 'IndexView, DetailView and ResultsView are classes now in views.py
# django expects the P to pass too be called <pk> for a generic as_view().

# reverse is like redirect in gae.
# If the URL accepts arguments, you may pass them in args.

# See the old way below.
# The new way:
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]

"""
Note that the name of the matched pattern in the regexes of the second
and third patterns has changed from <question_id> to <pk> above.

The old way.
urlpatterns = [
    # ex: /myPolls/
    url(r'^$', views.index, name='index'),

    # ex: /myPolls/5/
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),

    # ex: /myPolls/5/results/
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),

    # ex: /myPolls/5/vote/
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]

"""