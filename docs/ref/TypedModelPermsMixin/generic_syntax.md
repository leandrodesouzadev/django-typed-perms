# `TypedPermsModelMixin`

A mixin that can be used that adds extended functionality to a Django `Model` class. This mixin is a `Generic` type, that can take two optional arguments:

* the custom permissions; and
* the default permissions.

These arguments when provided will provide the exact available permissions for that Model. All of the following are **valid** usecases:

## Inheriting with no Generic arguments provided

This will cause that the Model only provide the default Django permissions, they are: `"add"`, `"change"`, `"delete"`, `"view"`. Example:
``` py title="polls/models.py" hl_lines="4"
from django.db import models
from django_typed_perms import TypedPermsModelMixin

class Question(TypedPermsModelMixin, models.Model):
    ...
```

## Inheriting with a single `Generic` argument provided

This will cause that the default Django permissions to be present (listed above), plus the ones that you define.

``` py title="polls/models.py" hl_lines="1 5 7 9-10"
from typing import Annotated, Literal
from django.db import models
from django_typed_perms import TypedPermsModelMixin, get_choices_from_type_hint

QuestionCustomPermsT = Annotated[Literal["publish_question"], "Publish Question"]

class Question(TypedPermsModelMixin[QuestionCustomPermsT], models.Model):
    
    class Meta:
        permissions = get_choices_from_type_hint(QuestionCustomPermsT)
```

!!! warning "Don't forget to add the `permissions` to the model's `Meta` class"
    
    If you forget to add the `permissions` to the `Meta` class, Django won't create the corresponding `Permission` when you run `python manage.py makemigrations`. If you forget to add, checking for a permission that doesn't exist will always return a `False` value.

!!! note "What's that `Annotated[Literal]` thing that I just saw?"
    
    Typing module `Annotated` allows you to associate any metadata you want to a specific type. In this case, the `Literal` type. With `Annotated` you can add as many metadata as you want to a type. But, in this case you're restricted just to a few, they're: `str`, a `None` value or a `gettext_lazy` call.
    `Literal` is a type that is saying that a value can only be that specific value.

`TypedPermsModelMixin` also allows a `Union` type of `Annotated` types. So if you have more than one custom permission, then you can use the following syntax:

``` py title="polls/models.py" hl_lines="1 5-8 10-12"
from typing import Annotated, Literal
from django.db import models
from django_typed_perms import TypedPermsModelMixin, get_choices_from_type_hint

QuestionCustomPermsT = (
    Annotated[Literal["publish_question"], "Publish Question"]
    | Annotated[Literal["clear_votes"], "Clear Votes"]
)

class Question(TypedPermsModelMixin[QuestionCustomPermsT], models.Model):
    class Meta:
        permissions = get_choices_from_type_hint(QuestionCustomPermsT)
```

The above sintax is the equivalent of the following syntax:

``` py title="polls/models.py" hl_lines="1 5-8 10-12"
from typing import Annotated, Literal, Union
from django.db import models
from django_typed_perms import TypedPermsModelMixin, get_choices_from_type_hint

QuestionCustomPermsT = Union[
    Annotated[Literal["publish_question"], "Publish Question"],
    Annotated[Literal["clear_votes"], "Clear Votes"],
]

class Question(TypedPermsModelMixin[QuestionCustomPermsT], models.Model):
    class Meta:
        permissions = get_choices_from_type_hint(QuestionCustomPermsT)
```

Feel free to use the syntax that you like the most.

## Inheriting with 2 `Generic` arguments provided

If you need to add custom permissions and also override the default permissions, then you can use the following syntax. For example, if you only want the `Question` model to have the `add` permission, you can:


``` py title="polls/models.py" hl_lines="9-11 16"
from typing import Annotated, Literal
from django.db import models
from django_typed_perms import TypedPermsModelMixin, get_choices_from_type_hint

QuestionCustomPermsT = (
    Annotated[Literal["publish_question"], "Publish Question"]
    | Annotated[Literal["clear_votes"], "Clear Votes"]
)
QuestionDefaultPermsT = (
    Annotated[Literal["add"], "Add Question"]
)

class Question(TypedPermsModelMixin[QuestionCustomPermsT, QuestionDefaultPermsT], models.Model):
    class Meta:
        permissions = get_choices_from_type_hint(QuestionCustomPermsT)
        default_permissions = get_choices_from_type_hint(QuestionDefaultPermsT)
```

Now the only 3 available permissions are: `publish_question`, `clear_votes`, and `add`.
