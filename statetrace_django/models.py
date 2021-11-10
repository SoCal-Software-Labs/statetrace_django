import uuid
from django.db import models
from django.db.models import JSONField as JSONBField
from django.utils import timezone
import time


def new_id():
    return str(uuid.uuid4())


class JSONField(JSONBField):
    def db_type(self, connection):
        return "json"


class Annotation(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    timestamp = models.DateTimeField()
    id = models.TextField()
    kind = models.TextField()

    meta = JSONField(null=True)
    payload = JSONField(null=True)

    class Meta:
        db_table = "statetrace_annotations"

    @classmethod
    def log_session(
        cls,
        actor_id=None,
        actor_full_name=None,
        actor_email=None,
        actor_avatar=None,
        client_user_agent=None,
        application_id=None,
        meta=None,
        timestamp=None,
    ):
        return Annotation.objects.create(
            kind="_st.app.sess",
            id=new_id(),
            timestamp=timestamp or timezone.now(),
            meta=meta,
            payload=dict(
                session_actor_id=actor_id and str(actor_id),
                session_actor_full_name=actor_full_name,
                session_actor_email=actor_email,
                session_actor_avatar=actor_avatar,
                session_client_user_agent=client_user_agent,
                session_application_id=application_id,
                session_application_type="python/django",
            )
        )

    @classmethod
    def log_action(
        cls,
        action_session_id,
        action_url=None,
        action_method=None,
        action_version=None,
        action_parent_id=None,
        meta=None,
        timestamp=None,
        action_length_ms=None,
    ):
        return Annotation.objects.create(
            kind="_st.app.act",
            id=new_id(),
            timestamp=timestamp or timezone.now(),
            meta=meta,
            payload=dict(
                action_session_id=action_session_id,
                action_url=action_url,
                action_method=action_method,
                action_version=action_version,
                action_length_ms=action_length_ms,
                action_parent_id=action_parent_id
            )
        )

    @classmethod
    def log_migration(
        cls,
        meta=None,
        timestamp=None,
    ):
        return Annotation.objects.create(
            kind="_st.app.mig",
            id=new_id(),
            timestamp=timestamp or timezone.now(),
            meta=meta
        )