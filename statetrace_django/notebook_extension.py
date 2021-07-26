from .thread import set_builder
from tracestate import TraceBuilder, client
from django.utils import timezone
from django.db import connection


class TraceStateWatcher(object):
    def __init__(self):
        self.builder = None

    def pre_run_cell(self, info):
        builder = TraceBuilder.new_frame(uri="console://ipython", actor=None)
        set_builder(builder)
        self.builder = builder
        with connection.cursor() as cursor:
            cursor.execute('set session "tracestate.request_id" = %s;', [builder.id])

    def post_run_cell(self, result):
        client.push([self.builder])
        set_builder(None)


def load_ipython_extension(ip):
    vw = TraceStateWatcher()
    ip.events.register("pre_run_cell", vw.pre_run_cell)
    ip.events.register("post_run_cell", vw.post_run_cell)


def unload_ipython_extension(ipython):
    # If you want your extension to be unloadable, put that logic here.
    pass
