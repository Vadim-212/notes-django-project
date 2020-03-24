from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django import forms
from django.contrib.auth.models import User
from notes.models import User as UserModel
from django.utils.translation import gettext as _
# import bcrypt


class RegisterForm(UserCreationForm):
    username = UsernameField(label=_("Username"))
    email = forms.EmailField(label=_("Email"))
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label=_("Confirm password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )
    error_messages = {
        'password_mismatch': _("Passwords don't match"),
    }

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", )


class LoginForm(forms.Form):
    username = forms.CharField(label=_("Username"))
    password = forms.CharField(widget=forms.PasswordInput, label=_("Password"))


class NoteForm(forms.Form):
    is_private = forms.BooleanField(label=_("Private"),initial=True,required=False)
    text = forms.CharField(label=_("Note text"),widget=forms.Textarea)


# class ModelBackend(BaseBackend):
#     """
#     Authenticates against settings.AUTH_USER_MODEL.
#     """
#
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         if username is None:
#             username = kwargs.get(UserModel.USERNAME_FIELD)
#         if username is None or password is None:
#             return
#         try:
#             user = UserModel._default_manager.get_by_natural_key(username)
#         except UserModel.DoesNotExist:
#             # Run the default password hasher once to reduce the timing
#             # difference between an existing and a nonexistent user (#20760).
#             UserModel().set_password(password)
#         else:
#             if user.check_password(password) and self.user_can_authenticate(user):
#                 return user
#
#     def user_can_authenticate(self, user):
#         """
#         Reject users with is_active=False. Custom user models that don't have
#         that attribute are allowed.
#         """
#         is_active = getattr(user, 'is_active', None)
#        return is_active or is_active is None


# def login(username, email, password):
#     pass_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
#     user = UserModel(login=username, email=email, password=pass_hash)
#     user.save()
#     return user
