from .models import Annotation
import json
import time
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.db import transaction
from django.conf import settings


def log_session(request):
    user = request.user
    print(request.user)
    return Annotation.log_session(
        actor_id=str(user.pk) if user.is_authenticated else "session-" +
        request.session.session_key,
        actor_full_name=(user.get_full_name() or user.username) if user.is_authenticated else None,
        actor_avatar=getattr(user, 'get_avatar', lambda: None)(),
        client_user_agent=request.META['HTTP_USER_AGENT'],
        application_id=getattr(settings, "STATETRACE_APPLICATION_ID", None)
    )


@receiver(user_logged_in)
def post_login(sender, user, request, **kwargs):

    print((user, request.user))
    annotation = log_session(request)
    request.session["_st.session"] = [str(annotation.timestamp), annotation.id]
    request.session.modified = True


def process_session_frame(request):
    if "_st.session" not in request.session:
        if not request.session.session_key:
            request.session.create()

        annotation = log_session(request)
        request.session["_st.session"] = [
            str(annotation.timestamp), annotation.id]
        request.session.modified = True
    return tuple(request.session["_st.session"])

def time_ms():
    return int(time.monotonic() * 1000)


def statetrace_middleware(get_response):
    application_version = getattr(settings, "STATETRACE_APPLICATION_VERSION", None)
    
    def middleware(request):

        (parent_timestamp, parent_id) = process_session_frame(request)

        with transaction.atomic():
            start = time_ms()
            response = get_response(request)
            Annotation.log_action(
                parent_timestamp,
                parent_id,
                action_url=request.build_absolute_uri(),
                action_method=request.method,
                action_version=application_version,
                frame_length_ms=time_ms() - start
            )
            return response

    return middleware
