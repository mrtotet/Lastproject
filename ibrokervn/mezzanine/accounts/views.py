from __future__ import unicode_literals

from django.contrib.auth import (login as auth_login, authenticate,
                                 logout as auth_logout, get_user_model)
from django.contrib.auth.decorators import login_required
from django.contrib.messages import info, error
from django.core.urlresolvers import NoReverseMatch, get_script_prefix
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _

from mezzanine.accounts import get_profile_form
from mezzanine.accounts.forms import LoginForm, PasswordResetForm, Signup_Form, ProfileForm
from mezzanine.conf import settings
from mezzanine.utils.email import send_verification_mail, send_approve_mail
from mezzanine.utils.urls import login_redirect, next_url


User = get_user_model()


def login(request, template="accounts/account_login.html",
          form_class=LoginForm, extra_context=None):
    """
    Login form.
    """
    form = form_class(request.POST or None)
    if request.method == "POST" and form.is_valid():
        authenticated_user = form.save()
        info(request, _("Đăng nhập thành công"))
        auth_login(request, authenticated_user)
        return login_redirect(request)
    context = {"form": form, "title": _("Đăng nhập")}
    context.update(extra_context or {})
    return TemplateResponse(request, template, context)


def logout(request):
    """
    Log the user out.
    """
    auth_logout(request)
    info(request, _("Đăng xuất thành công"))
    return redirect(next_url(request) or get_script_prefix())


def signup(request, template="accounts/account_signup.html",form_class=Signup_Form,
           extra_context=None):
    """
    Signup form.
    """
    #profile_form = get_profile_form()   #dùng cách này để tách sign up và update profile ra làm 2
    #form = profile_form(request.POST or None, request.FILES or None)   #và update profile ra làm 2
    form = form_class(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        new_user = form.save()
        if not new_user.is_active:
            if settings.ACCOUNTS_APPROVAL_REQUIRED:
                send_approve_mail(request, new_user)
                info(request, _("Cảm ơn đã đăng ký! Bạn sẽ được nhận "
                                "email thông báo khi tài khoản được kích hoạt"))
            else:
                send_verification_mail(request, new_user, "signup_verify")
                info(request, _("Một email với link xác nhận đã được gửi "
                                "hãy nhấp vào đường link để kích hoạt tài khoản"))
            return redirect(next_url(request) or "/")
        else:
            info(request, _("Đăng ký thành công"))
            auth_login(request, new_user)
            return login_redirect(request)
    context = {"form": form, "title": _("Đăng ký tài khoản mới")}
    context.update(extra_context or {})
    return TemplateResponse(request, template, context)


def signup_verify(request, uidb36=None, token=None):
    """
    View for the link in the verification email sent to a new user
    when they create an account and ``ACCOUNTS_VERIFICATION_REQUIRED``
    is set to ``True``. Activates the user and logs them in,
    redirecting to the URL they tried to access when signing up.
    """
    user = authenticate(uidb36=uidb36, token=token, is_active=False)
    if user is not None:
        user.is_active = True
        user.save()
        auth_login(request, user)
        info(request, _("Đăng ký thành công"))
        return login_redirect(request)
    else:
        error(request, _("Đường link vừa nhấp không còn hiệu lực"))
        return redirect("/")


@login_required
def profile_redirect(request):
    """
    Just gives the URL prefix for profiles an action - redirect
    to the logged in user's profile.
    """
    return redirect("profile", username=request.user.username)


def profile(request, username, template="accounts/account_profile.html",
            extra_context=None):
    """
    Display a profile.
    """
    lookup = {"username__iexact": username, "is_active": True}
    context = {"profile_user": get_object_or_404(User, **lookup)}
    context.update(extra_context or {})
    return TemplateResponse(request, template, context)


@login_required
def account_redirect(request):
    """
    Just gives the URL prefix for accounts an action - redirect
    to the profile update form.
    """
    return redirect("profile_update")


@login_required
def profile_update(request, template="accounts/account_profile_update.html",
                   #form_class=ProfileForm,
                    #form_class=Signup_Form,
                   extra_context=None):
    """
    Profile update form.
    """
    profile_form = get_profile_form()   #dùng cách này để tách sign up và update profile ra làm 2
    form = profile_form(request.POST or None, request.FILES or None,instance=request.user)   #và update profile ra làm 2
    #form = form_class(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        info(request, _("Profile updated"))
        try:
            return redirect("profile", username=user.username)
        except NoReverseMatch:
            return redirect("profile_update")
    context = {"form": form, "title": _("Cập nhật Profile")}
    context.update(extra_context or {})
    return TemplateResponse(request, template, context)


def password_reset(request, template="accounts/account_password_reset.html",
                   form_class=PasswordResetForm, extra_context=None):
    form = form_class(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        send_verification_mail(request, user, "password_reset_verify")
        info(request, _("Một email với đượng link vừa được gửi "
                        "nhấp vào đường link để reset password"))
    context = {"form": form, "title": _("Password Reset")}
    context.update(extra_context or {})
    return TemplateResponse(request, template, context)


def password_reset_verify(request, uidb36=None, token=None):
    user = authenticate(uidb36=uidb36, token=token, is_active=True)
    if user is not None:
        auth_login(request, user)
        return redirect("profile_update")
    else:
        error(request, _("Đường link vừa nhấp không còn hiệu lực."))
        return redirect("/")
