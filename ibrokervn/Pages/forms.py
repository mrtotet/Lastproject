from __future__ import unicode_literals

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Q
from django.db.models.manager import Manager
from django import forms
from django.utils.http import int_to_base36
from django.utils.translation import ugettext, ugettext_lazy as _

from mezzanine.accounts import (get_profile_model, get_profile_user_fieldname,
                                get_profile_for_user, ProfileNotConfigured)
from mezzanine.conf import settings
from mezzanine.core.forms import Html5Mixin
from mezzanine.utils.urls import slugify, unique_slug


User = get_user_model()

_exclude_fields = tuple(getattr(settings,
                                "ACCOUNTS_PROFILE_FORM_EXCLUDE_FIELDS", ()))


try:
    class ProfileFieldsForm(forms.ModelForm):
        class Meta:
            model = get_profile_model()
            exclude = (get_profile_user_fieldname(),) + _exclude_fields
except ProfileNotConfigured:
    pass


if settings.ACCOUNTS_NO_USERNAME:
    _exclude_fields += ("username",)
    username_label = _("Email address")
else:
    username_label = _("Username or email address")


class LoginForm(Html5Mixin, forms.Form):

    username = forms.CharField(label=username_label)
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput(render_value=False))

    def clean(self):

        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        self._user = authenticate(username=username, password=password)
        if self._user is None:
            raise forms.ValidationError(
                             ugettext("username/email hoặc password không tồn tại "))
        elif not self._user.is_active:
            raise forms.ValidationError(ugettext("Tài khoản chưa kích hoạt"))
        return self.cleaned_data

    def save(self):
        return getattr(self, "_user", None)


class ProfileForm(Html5Mixin, forms.ModelForm):

    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(label=_("Password (again)"),
                                widget=forms.PasswordInput(render_value=False))

    class Meta:
        model = User
        fields = ("họ và tên", "email", "username")
        exclude = _exclude_fields

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self._signup = self.instance.id is None
        user_fields = set([f.name for f in User._meta.get_fields()])
        try:
            self.fields["username"].help_text = ugettext(
                        "Chỉ bảo gồm chữ, số dấu '_' hoặc dấu '_' ")
        except KeyError:
            pass
        for field in self.fields:
            # Make user fields required.
            if field in user_fields:
                self.fields[field].required = True
            # Disable auto-complete for password fields.
            # Password isn't required for profile update.
            if field.startswith("password"):
                self.fields[field].widget.attrs["autocomplete"] = "off"
                self.fields[field].widget.attrs.pop("thôn tin bắt buộc", "")
                if not self._signup:
                    self.fields[field].required = False
                    if field == "password1":
                        self.fields[field].help_text = ugettext(
                                               "Để trống trừ khi "
                                               "muốn đổi password mới")

        # Add any profile fields to the form.
        try:
            profile_fields_form = self.get_profile_fields_form()
            profile_fields = profile_fields_form().fields
            self.fields.update(profile_fields)
            if not self._signup:
                user_profile = get_profile_for_user(self.instance)
                for field in profile_fields:
                    value = getattr(user_profile, field)
                    # Check for multiple initial values, i.e. a m2m field
                    if isinstance(value, Manager):
                        value = value.all()
                    self.initial[field] = value
        except ProfileNotConfigured:
            pass

    def clean_username(self):

        username = self.cleaned_data.get("username")
        if username.lower() != slugify(username).lower():
            raise forms.ValidationError(
                ugettext("Username can only contain letters, numbers, dashes "
                         "or underscores."))
        lookup = {"username__iexact": username}
        try:
            User.objects.exclude(id=self.instance.id).get(**lookup)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
                            ugettext("username này đã được sử dụng"))

    def clean_password2(self):

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1:
            errors = []
            if password1 != password2:
                errors.append(ugettext("Passwords nhập lại không khớp"))
            if len(password1) < settings.ACCOUNTS_MIN_PASSWORD_LENGTH:
                errors.append(
                        ugettext("Password must be at least %s characters") %
                        settings.ACCOUNTS_MIN_PASSWORD_LENGTH)
            if errors:
                self._errors["password1"] = self.error_class(errors)
        return password2

    def clean_email(self):

        email = self.cleaned_data.get("email")
        qs = User.objects.exclude(id=self.instance.id).filter(email=email)
        if len(qs) == 0:
            return email
        raise forms.ValidationError(
                                ugettext("email này đã sử dụng"))

    def save(self, *args, **kwargs):
        kwargs["commit"] = False
        user = super(ProfileForm, self).save(*args, **kwargs)
        try:
            self.cleaned_data["username"]
        except KeyError:
            if not self.instance.username:
                try:
                    username = ("%(first_name)s %(last_name)s" %
                                self.cleaned_data).strip()
                except KeyError:
                    username = ""
                if not username:
                    username = self.cleaned_data["email"].split("@")[0]
                qs = User.objects.exclude(id=self.instance.id)
                user.username = unique_slug(qs, "username", slugify(username))
        password = self.cleaned_data.get("password1")
        if password:
            user.set_password(password)
        elif self._signup:
            try:
                user.set_unusable_password()
            except AttributeError:

                pass
        user.save()

        try:
            profile = get_profile_for_user(user)
            profile_form = self.get_profile_fields_form()
            profile_form(self.data, self.files, instance=profile).save()
        except ProfileNotConfigured:
            pass

        if self._signup:
            if (settings.ACCOUNTS_VERIFICATION_REQUIRED or
                    settings.ACCOUNTS_APPROVAL_REQUIRED):
                user.is_active = False
                user.save()
            else:
                token = default_token_generator.make_token(user)
                user = authenticate(uidb36=int_to_base36(user.id),
                                    token=token,
                                    is_active=True)
        return user

    def get_profile_fields_form(self):
        try:
            return ProfileFieldsForm
        except NameError:
            raise ProfileNotConfigured


class PasswordResetForm(Html5Mixin, forms.Form):

    username = forms.CharField(label=username_label)

    def clean(self):
        username = self.cleaned_data.get("username")
        username_or_email = Q(username=username) | Q(email=username)
        try:
            user = User.objects.get(username_or_email, is_active=True)
        except User.DoesNotExist:
            raise forms.ValidationError(
                             ugettext("username/email không tồn tại"))
        else:
            self._user = user
        return self.cleaned_data

    def save(self):

        return getattr(self, "_user", None)
