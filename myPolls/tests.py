
# Create your tests here.

import datetime

from django.utils import timezone

# The client method comes from here as well as other stuff.
from django.test import TestCase

from .models import Question
from django.urls import reverse


# django will automatically run these tests when you run
# 'python manage.py test myPolls' from bash /mysite
# It sets up its own temporary db to do this.

class QuestionMethodTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future.  var time is 30 days in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is older than 1 day. var time is 30 days in the past.
        """

        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() should return True for questions whose
        pub_date is within the last day.  var time is one hour ago.
        """
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


###################### End Class QuestionMethodTests



def create_question(question_text, days):
    """
    Creates a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """

# var days is how many days to add/subtract from timezone.now()
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionViewTests(TestCase):
    def test_index_view_with_no_questions(self):
        """
        If no questions exist, an appropriate message should be displayed.
        This refers to the message that the html displays.
        """

# 'myPolls:index' refers to /myPolls/url.py name = 'index'
        """
        urlpatterns = [
            url(r'^$', views.IndexView.as_view(), name='index'),
            url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(),
                                                  name='detail'),...
        """
# reverse is like redirect in gae.  If the url takes arguments
# like that regexp above then you can pass them as args= 'value'
# reverse('myPolls:detail', args = '5746478')
# import TestCase gives us client. A robotic/fake user.
        response = self.client.get(reverse('myPolls:index'))
        self.assertEqual(response.status_code, 200)

# The words "No polls are available." are coming from
# line 36 at index.html, it is the print out if no polls are availabe.

        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_a_past_question(self):
        """
        Questions with a pub_date in the past should be displayed on the
        index page.
        """
        create_question(question_text="Past question Davee.", days=-30)
        response = self.client.get(reverse('myPolls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],  # content

# The  '<Question: Past question Davee.>' is a Question object created
# at line 98 with a call to the helper function create_question at line
# 54.
# The "Past question Davee." part comes from line 98 above.
            ['<Question: Past question Davee.>']  # context
        )
    """
    From half way down in the tutorial, this explains the above Question...
    >>> response = client.get(reverse('polls:index'))
    >>> response.status_code
    200

    >>> response.content
    b'\n    <ul>\n    \n        <li><a href="/polls/1/">What&#39;s up?</a></li>\n    \n    </ul>\n\n'

    >>> response.context['latest_question_list']
    <QuerySet [<Question: What's up?>]>

    """



    def test_index_view_with_a_future_question(self):
        """
        Questions with a pub_date in the future should not be displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('myPolls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        should be displayed.
        """
        create_question(question_text="Past question DaveeJ.", days=-30)
        create_question(question_text="Future question.", days=30)

        response = self.client.get(reverse('myPolls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],

            ['<Question: Past question DaveeJ.>']
        )

    def test_index_view_with_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)

        response = self.client.get(reverse('myPolls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )


###################### End QuestionViewTests



class QuestionIndexDetailTests(TestCase):
    def test_detail_view_with_a_future_question(self):
        """
        The detail view of a question with a pub_date in the future should
        return a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('myPolls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_question(self):
        """
        The detail view of a question with a pub_date in the past should
        display the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5)

# How does reverse work, why is there an argument.  The detail url
# has a regexp in front of it, it looks for a number.  See url.py
# and index.html for hints.
        url = reverse('myPolls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


########################### End QuestionIndexDetailTests





