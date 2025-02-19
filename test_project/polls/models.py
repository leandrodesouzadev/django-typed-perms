from datetime import timedelta
from typing import Annotated, Literal


from django.contrib import admin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_typed_perms import TypedPermsModelMixin, get_choices_from_type_hint


QuestionCustomPerms = (
    Annotated[Literal["change_pub_date"], _("Can change pub_date")]
    | Annotated[Literal["add_choices"], "Add choices"]
)


class Question(TypedPermsModelMixin[QuestionCustomPerms], models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    class Meta:
        permissions = get_choices_from_type_hint(QuestionCustomPerms)

    def __str__(self):
        return self.question_text

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
