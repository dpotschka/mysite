# And speaking of forms with dozens of fields, you might
# want to split the form up into fieldsets:
# This puts a nice blue bar befor each category/field,
# with the name of the field in the bar.
# The first element of each tuple in fieldsets is the
# title of the fieldset.
# --

"""
admin.site.register(Choice)
In that form, the "Question" field is a select box
containing every question in the database. Django knows
that a ForeignKey should be represented in the admin as a <select> box.
"""

# See here for all the cool formatting options provided by
# Django used below.
# https://docs.djangoproject.com/en/1.10/intro/tutorial07/

from django.contrib import admin

from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
#class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes':
                                                        ['collapse']}),
    ]
    inlines = [ChoiceInline]

    list_display = ('question_text', 'pub_date', 'was_published_recently')
    """
    You can click on the column headers to sort by those values - except
    in the case of the was_published_recently header, because sorting
    by the output of an arbitrary method is not supported. Also note
    that the column header for was_published_recently is, by default,
    the name of the method (with underscores replaced with spaces),
    and that each line contains the string representation of the output.
    """

    list_filter = ['pub_date']
    """
    That adds a 'Filter' sidebar that lets people filter
    the change list by the pub_date field.

    The type of filter displayed depends on the type of field you're
    filtering on. Because pub_date is a DateTimeField, Django knows
    to give appropriate filter options: 'Any date', 'Today', 'Past 7
    days', 'This month', 'This year'.
    """

# Adds a search bar, use as many fields from your db as you want,
# to many and it slows the search down.
# Default is to display 100 items per page.
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)



"""

The old ways.

from django.contrib import admin

from .models import Question


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]

admin.site.register(Question, QuestionAdmin)

--


from django.contrib import admin

from .models import Question

# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
    fields = ['pub_date', 'question_text']

admin.site.register(Question, QuestionAdmin)

admin.site.register(Choice)
In that form, the "Question" field is a select box
containing every question in the database. Django knows
that a ForeignKey should be represented in the admin as a <select> box.

--


from django.contrib import admin

# Register your models here.
from .models import Question

admin.site.register(Question)

admin.site.register(Choice)
In that form, the 'Question' field is a select box
containing every question in the database. Django knows
that a ForeignKey should be represented in the admin as a <select> box.


"""








