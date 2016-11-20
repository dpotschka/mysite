from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Choice, Question

from django.utils import timezone

from django.views import generic



# Create your views here.

# Using generic views from Lesson 4 at:
# https://docs.djangoproject.com/en/1.10/intro/tutorial04/
# Next, we're going to remove our old index, detail, and results
# views and use Django's generic views instead.

# I put most of the documentation from the tutorial after these
# class definitions (with corrections I might add).  READ IT OFTEN.
# Basically Django can take a class definition and a db model
# and fill in your template.html automatically with "generic views".

# I also believe it automatically runs any functions within a class
# declaration using the as_view() imported
# "from django.views import generic" (above) via the the url mapper at:
# /mysite/myPolls/urls.py


class IndexView(generic.ListView):
    """ context_object_name, template_name and get_queryset() are all
    django dependant.  They all work together to pass info to the
    index.html.  You can pass whatever you want.
    """

    template_name = 'myPolls/index.html'

# Use the  context_object_name 'latest_question_list' to pass the
# db rows/field/object returned from the get_queryset() to index.html
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not
        including those set to be published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


"""
In previous parts of the tutorial, the templates have been
provided with a context that contains the question and
latest_question_list context variables. For DetailView
the question variable is provided automatically - since

we're using a Django model (Question), Django is able to
determine an appropriate name for the context variable (ie Davee 'question').

I am going to over-ride that because it is a dumb idea (very confusing).
  I have added
context_object_name = 'latest'

The original class DetailView had no such declaration yet django was 
able to find 'question' var in the detail.html file.

However, for ListView, the automatically generated context
variable is question_list. To override this we provide the

context_object_name attribute, specifying that we want to use
latest_question_list instead (as it is named in our index.html file).
As an alternative approach, you
could change your templates to match the new default context
variables - but it's a lot easier to just tell Django to
use the variable you want.
"""

class DetailView(generic.DetailView):
    # The db to use in the template.
    #model = Question
    
    template_name = 'myPolls/detail.html' 

# I add this here and to the detail.html file although everything worked
# before with out it!  Your default var had to be all lowercase 'question'.
# This is also used by the vote() to pass vars.
    context_object_name = 'latest'
    
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())



"""
This is what the form runs at detail.html
"""
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'myPolls/detail.html', {
            'latest': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
# Always return an HttpResponseRedirect after successfully dealing
# with POST data. This prevents data from being posted twice if a
# user hits the Back button.  # reverse is like redirect in gae.
# If the URL accepts arguments a regexp say,
# you may pass them in args.
        return HttpResponseRedirect(  reverse( 'myPolls:results', args=(question.id,) )  )



class ResultsView(generic.DetailView):
    model = Question
    template_name = 'myPolls/results.html'






"""
We're using two generic views here: ListView and DetailView.
Respectively, those two views abstract the concepts
of "display a list of objects" and "display a detail page
for a particular type of object."

Each generic view needs to know what model it will be acting
upon. This is provided using the model attribute.
The DetailView generic view expects the primary key value captured
from the URL to be called "pk", so we've changed question_id to pk

for the generic views in the url mapper found at:
/mysite/myPolls/urls.py

By default, the DetailView generic view uses
a template called <app name>/<model name>_detail.html. In
our case, it would use the template "myPolls/question_detail.html".
The template_name attribute is used to tell Django to use
a specific template name instead of the autogenerated default template
name.

We also specify the template_name for the results list
view - this ensures that the results view and the detail view
have a different appearance when rendered, even though they're
both a DetailView behind the scenes.

Similarly, the ListView generic view uses a default template
called <app name>/<model name>_list.html; we use template_name to
tell ListView to use our existing "myPolls/index.html" template.

In previous parts of the tutorial, the templates have been
provided with a context that contains the question and
latest_question_list context variables. For DetailView
the question variable is provided automatically - since

we're using a Django model (Question), Django is able to
determine an appropriate name for the context variable.
However, for ListView, the automatically generated context
variable is question_list. To override this we provide the

context_object_name attribute, specifying that we want to use
latest_question_list instead (as it is named in our index.html file).
As an alternative approach, you
could change your templates to match the new default context
variables - but it's a lot easier to just tell Django to
use the variable you want.

"""


"""
The older ways of doing everything.

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'myPolls/detail.html', {'question': question})

The old ways for detail().

#from django.http import Http404, HttpResponse

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'myPolls/detail.html', {'question': question})

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)
####

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'myPolls/results.html', {'question': question})

The old way.
def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

####


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'myPolls/index.html', context)

The old ways of doing it.

from django.template import loader

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('myPolls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

"""












