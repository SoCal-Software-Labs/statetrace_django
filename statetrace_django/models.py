import uuid
from .utils import new_id
from django.db import models
from django.db.models import JSONField as JSONBField
from django.utils import timezone


class JSONField(JSONBField):
    def db_type(self, connection):
        return "json"


class Annotation(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    timestamp = models.DateTimeField()
    id = models.IntegerField()
    kind = models.TextField()

    frame_length_ms = models.IntegerField(null=True)
    meta = JSONField(null=True)
    parent_id = models.IntegerField(null=True)
    parent_timestamp = models.DateTimeField(null=True)

    action_url = models.TextField(null=True)
    action_method = models.TextField(null=True)
    action_version = models.TextField(null=True)

    session_client_user_agent = models.TextField(null=True)
    session_application_type = models.TextField(null=True)
    session_application_id = models.TextField(null=True)
    session_actor_id = models.TextField(null=True)
    session_actor_full_name = models.TextField(null=True)
    session_actor_avatar = models.TextField(null=True)

    class Meta:
        db_table = "statetrace_annotations"

    @classmethod
    def log_session(
        cls,
        actor_id=None,
        actor_full_name=None,
        actor_avatar=None,
        client_user_agent=None,
        application_id=None,
        meta=None,
        timestamp=None,
    ):
        return Annotation.objects.create(
            kind="_st.app.sess",
            session_application_type="python/django",
            id=new_id(),
            timestamp=timestamp or timezone.now(),
            meta=meta,
            session_actor_id=actor_id and str(actor_id),
            session_actor_full_name=actor_full_name,
            session_actor_avatar=actor_avatar,
            session_client_user_agent=client_user_agent,
            session_application_id=application_id,
        )

    @classmethod
    def log_action(
        cls,
        parent_timestamp,
        parent_id,
        action_url=None,
        action_method=None,
        action_version=None,
        meta=None,
        timestamp=None,
        frame_length_ms=None,
    ):
        return Annotation.objects.create(
            kind="_st.app.act",
            id=new_id(),
            timestamp=timestamp or timezone.now(),
            parent_id=parent_id,
            parent_timestamp=parent_timestamp,
            meta=meta,
            action_url=action_url,
            action_method=action_method,
            action_version=action_version,
            frame_length_ms=frame_length_ms,
        )
