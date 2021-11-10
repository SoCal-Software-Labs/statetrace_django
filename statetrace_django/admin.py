from django.contrib import admin

from django.conf import settings


class StateTraceAdmin(admin.ModelAdmin):

    change_form_template = "statetrace_django/change_form.html"

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = {
            **(extra_context or {}),
            **{
                "staterace_search_base_url": getattr(
                    settings,
                    "STATETRACE_SEARCH_URL",
                    "http://localhost:4000/organizations/1/environments/1/db/1/outbound/1/search",
                ),
                "statetrace_object_pk": object_id,
                "statetrace_table_name": self.model._meta.db_table,
            },
        }
        return super().change_view(request, object_id, form_url, extra_context)
