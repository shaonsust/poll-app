"""This is the controller for poll app."""
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice


class IndexView(generic.ListView):                                                  # pylint: disable=too-many-ancestors
    """This view for index page which will see question list."""

    template_name = "polls/index.html"
    context_object_name = "question_list"

    def get_queryset(self):
        """:return the last five published Question"""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by(      # pylint: disable=no-member
            "-pub_date"
        )[:5]


class DetailView(generic.DetailView):                                               # pylint: disable=too-many-ancestors
    """
    This view for details view
    """

    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Only published question will return, Future question will not return here.
        :return:
        """
        return Question.objects.filter(pub_date__lte=timezone.now())                # pylint: disable=no-member


class ResultsView(generic.DetailView):                                              # pylint: disable=too-many-ancestors
    """
    This view is for showing result.
    """

    model = Question
    template_name = "polls/results.html"

    def get_queryset(self):
        """
        Only published question's result can be seen.
        :return:
        """
        return Question.objects.filter(pub_date__lte=timezone.now())                 # pylint: disable=no-member


def vote(request, question_id):
    """
    Only for voting.
    :param request:
    :param question_id:
    :return:
    """

    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):                                          # pylint: disable=no-member
        # Redisplay voting form
        return render(
            request,
            "polls/detail.html",
            {"question": question, "error_message": "you did not choose a choice."},
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with post data. This prevents data being posted twice if the
        # user hits the back button
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
