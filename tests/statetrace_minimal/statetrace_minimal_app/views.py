from django.http import HttpResponse
from .models import MyModel


def query_model(request):
    objs = list(MyModel.objects.all())
    return HttpResponse("ok")


def change_model(request):
    created = MyModel.objects.create(name="Some Name")
    return HttpResponse("ok")


def multiple_queries(request):
    objs = list(MyModel.objects.all())
    objs = list(MyModel.objects.all()[1:])
    return HttpResponse("ok")
