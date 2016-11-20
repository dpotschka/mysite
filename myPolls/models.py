from django.db import models
from django.utils.encoding import python_2_unicode_compatible
import datetime
from django.utils import timezone


# Create your models here.

@python_2_unicode_compatible  # For python 2 support.
class Question(models.Model):
    question_text = models.CharField(max_length=200)

    # The field name would have been 'pub_date' but we set it to
    #                               'date published'
    pub_date = models.DateTimeField('date published')

    # returns a string instead of a reference to an object.
    # You also need this for the decorator above.
    def __str__(self):
        return self.question_text

    # Published within the last 24 hours.
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    # The search order?
    was_published_recently.admin_order_field = 'pub_date'

    # A default?
    was_published_recently.boolean = True

    was_published_recently.short_description = 'Published recently?'


@python_2_unicode_compatible
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


