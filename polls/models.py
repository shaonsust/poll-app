"""
Here have two Models named Question and Choice
"""

import datetime
from django.db import models
from django.utils import timezone


# Create your models here.
class Question(models.Model):
    """
    Question Model
    """

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        """
        Checking Question published recently or not
        :return: boolean
        """

        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")


class Choice(models.Model):
    """
    Choice Model
    """

    def __str__(self):
        return self.choice_text

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
