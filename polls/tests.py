"""
Model Testing
"""

import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


# Create your tests here.
class QuestionModelTests(TestCase):
    """
    Testing Question Model
    """

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() will return False if pub_date
        in the future.
        """
        time = timezone.now() + datetime.timedelta(days=1, seconds=1)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() will return False if
        pub_date is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() will return true if
        pub_date is within 1 day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    """
    Create a Question with the given question_text and
    published the given days offset to now.
    :param question_text:
    :param days:
    :return:
    """
    pub_date = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=pub_date)    # pylint: disable=no-member


class QuestionIndexViewTest(TestCase):
    """
    Question index view test.
    """

    def test_no_question(self):
        """
        If no question exist, an appropriate message will return
        :return:
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["question_list"], [])

    def test_past_question(self):
        """
        Question with a publish date in the past are displayed on the index page.
        :return:
        """
        create_question("Past question?", -30)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["question_list"], ["<Question: Past question?>"]
        )

    def test_future_question(self):
        """
        Question with a future pub_date will not show on the index page.
        :return:
        """
        create_question("future_question", 30)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["question_list"], [])

    def test_past_and_future_question(self):
        """
        Only past question will show on the index page
        :return:
        """
        create_question("future question.", 30)
        create_question("past question", -30)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["question_list"], ["<Question: past question>"]
        )

    def test_two_past_question(self):
        """
        Two past question will show on the index page.
        :return:
        """
        create_question("past question1.", -15)
        create_question("past question2.", -20)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["question_list"],
            ["<Question: past question1.>", "<Question: past question2.>"],
        )


class QuestionDetailViewTest(TestCase):
    """
    Question details view test
    """

    def test_future_question(self):
        """
        The detail view of a question with publish date in the future will
        return 404 status code.
        :return:
        """
        future_question = create_question("future question.", 15)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with publish date in the past will
        return the question text.
        :return:
        """
        past_question = create_question("past question.", -30)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, past_question)


class QuestionResultViewTest(TestCase):
    """
    Question results view test
    """

    def test_future_question_result(self):
        """
        The result view of question with publish date in the future will
        return 404 status code.
        :return:
        """
        future_question = create_question("Future question.", 30)
        url = reverse("polls:results", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question_result(self):
        """
        The result of a question with publish date in the past will
        return the question text.
        :return:
        """
        past_question = create_question("past question.", -20)
        url = reverse("polls:results", args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, past_question)
