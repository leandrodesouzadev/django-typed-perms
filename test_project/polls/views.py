from django.core.exceptions import PermissionDenied
from django.shortcuts import render

from polls.models import Question


def get_polls(request):
    if not Question.user_has_permission(request.user, ""):
        raise PermissionDenied
    return render(request, "polls/list.html")
