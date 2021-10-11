from .models import Annotation
import json
import time
import importlib
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.db import transaction
from django.conf import settings


def default_filter_func(request):
    return request.method in ["POST", "PUT", "DELETE", "PATCH"]


def default_meta_func(request):
    return None


def string_to_func(s, default):
    if s:
        mod_name, func_name = s.rsplit(".", 1)
        mod = importlib.import_module(mod_name)
        return getattr(mod, func_name)
    return default


statetrace_session_meta_func_name = getattr(settings, "STATETRACE_SESSION_META", None)
statetrace_action_meta_func_name = getattr(settings, "STATETRACE_ACTION_META", None)
statetrace_filter_func_name = getattr(settings, "STATETRACE_REQUEST_FILTER", None)
statetrace_session_meta_func = string_to_func(
    statetrace_session_meta_func_name, default_meta_func
)
statetrace_action_meta_func = string_to_func(
    statetrace_action_meta_func_name, default_meta_func
)
statetrace_filter_func = string_to_func(
    statetrace_filter_func_name, default_filter_func
)


def log_session(request):
    user = request.user
    session_meta = statetrace_session_meta_func(request)
    return Annotation.log_session(
        actor_id=str(user.pk)
        if user.is_authenticated
        else "session-" + request.session.session_key,
        actor_email=user.email
        if user.is_authenticated
        else None,
        actor_full_name=(user.get_full_name() or user.username)
        if user.is_authenticated
        else None,
        actor_avatar=getattr(user, "get_avatar", lambda: None)(),
        client_user_agent=request.META["HTTP_USER_AGENT"],
        application_id=getattr(settings, "STATETRACE_APPLICATION_ID", None),
        meta=session_meta,
    )


@receiver(user_logged_in)
def post_login(sender, user, request, **kwargs):
    annotation = log_session(request)
    request.session["_st.session"] = [str(annotation.timestamp), annotation.id]
    request.session.modified = True


def process_session_frame(request):
    if "_st.session" not in request.session:
        if not request.session.session_key:
            request.session.create()

        annotation = log_session(request)
        request.session["_st.session"] = [str(annotation.timestamp), annotation.id]
        request.session.modified = True
    return tuple(request.session["_st.session"])


def time_ms():
    return int(time.monotonic() * 1000)


def statetrace_middleware(get_response):
    application_version = getattr(settings, "STATETRACE_APPLICATION_VERSION", None)

    def middleware(request):

        (parent_timestamp, parent_id) = process_session_frame(request)

        if statetrace_filter_func(request):
            with transaction.atomic():
                start = time_ms()
                action_meta = statetrace_action_meta_func(request)

                response = get_response(request)

                Annotation.log_action(
                    action_session_id=parent_id,
                    action_url=request.build_absolute_uri(),
                    action_method=request.method,
                    action_version=application_version,
                    action_length_ms=time_ms() - start,
                    meta=action_meta,
                )
                return response
        else:
            return get_response(request)

    return middleware
