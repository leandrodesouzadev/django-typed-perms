The `TypedPermsModelMixin` class adds 3 methods to the inherited class. They're described below.

## Model definition used on examples

All of the code examples that uses these methods assumes the following model definition:
``` py title="polls/models.py"
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

## `user_has_permission`

This method is used to check a given `user` has the permission to do some `action` on that specific `Model` class or object. You can use this method as a type-safe replacement for `user.has_perm` method from `django.contrib.auth.models.AbstractUser`. The key difference, is that since you'll be using a specific class to check permissions for, then you only be able to check for an `action` of that specific class.

Imagine the following permission check, we want to check if the user has permission to `view` the `Question` objects. This is a default permission of any Django model. So, using the `user.has_perm` method, you would do the following:

``` py title="polls/views.py" hl_lines="2"
def get_polls(request):
    if not request.user or not request.user.has_perm("polls.view_question"):
        # Raise an error, missing permissions
        ...
```

If you have ever done a Django project before, you recognize this pattern. And you know this can get really annoying, if you do some easy mistakes, like:

* Don't checking for a `None` value on `request.user` (Some `AuthenticationBackend` could've assigned `None` as value), and that would result on a `TypeError`.
* Mispelling the permission `codename` (that is `{app_name}.{action}_{model_name}`) on entirety, or any of its pieces. This would result on a possible false positive.
* This is repetitive, and not developer-friendly.

Now, let's do the same permission check using the `user_has_permission` method.

``` py title="polls/views.py" hl_lines="4"
from polls.models import Question

def get_polls(request):
    if not Question.user_has_permission(request.user, "view"):
        # Raise an error, missing permissions
        ...
```

The same result, but way less things to type, and to make a mistake. When using this method, you don't have to:
* Worry about checking `request.user` for a `None` value;
* Worry about mispelling the exact permission `codename`, or the `app_name`, or the `action` name, or the `model_name`. If you're using `mypy` you'll get an error if you provide a invalid `action`.

### method signature

This method requires 2 positional/keyword arguments, they are:
* `user`: An `user-like` object or `None`. Meaning that this object must have the `has_perm` method.
* `action`: The name of the action to check permission against. This is either one of the Django's default permission, such as `add`, `change`, `delete`, or `view`.

It also optionally accepts a 3rd argument, the `obj` to check the permission against, we don't do anything with this argument, its directly passed to the `user.has_perm` method.


## `user_has_permissions`

This method is essentially the same as the method, above, the only difference is that instead of calling `user.has_perm`, it calls `user.has_perms` with the provided `Sequence` of `actions` provided (such as `tuple` or a `list`).

``` py title="polls/views.py" hl_lines="2"
def get_polls(request):
    if not Question.user_has_permissions(request.user, ("view", "add")):
        # Raise an error, missing permissions
        ...
```

## `get_action_permission_name`

This method can be used to retrieve the full qualified name of a permission, that can be used on `user.has_perm` call, for example. It accepts a single argument: `action` that is one of the Django's default permissions or any of the custom permissions provided on the mixin. This method is used internally by the methods `user_has_permission` and `user_has_permissions` to build the full permission name. Example:

``` py title="polls/views.py" hl_lines="2"
def get_polls(request):
    if not request.user not request.user.has_perm(Question.get_action_permission_name("view")):
        # Raise an error, missing permissions
        ...
```

This is the exact same of typing the full permission `codename`, such as:

``` py title="polls/views.py" hl_lines="2"
def get_polls(request):
    if not request.user not request.user.has_perm("polls.view_question"):
        # Raise an error, missing permissions
        ...
```
