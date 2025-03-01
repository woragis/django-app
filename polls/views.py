from django.db.models import F
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Question, Choice
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.username
        token['email'] = user.email

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "You have access!"})


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_name"

    def get_queryset(self):
        """
        Return the last five published questions.
        return Question.objects.order_by("-pub_date")[:5]
        """
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=now()).order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    # template = loader.get_template("polls/index.html")
    context = {"latest_question_list": latest_question_list}
    # return HttpResponse(template.render(context, request))
    return render(request, "polls/index.html", context)


def detail(request, question_id):
    """
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question doesnt exist")
    # return HttpResponse("You are looking at %s." % question_id)
    """
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html", {
            "question": question,
            "error_message": "You didn't selected a choice"
        })
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id)))
    response = "You are voting on question %s."
    return HttpResponse(response % question_id)
