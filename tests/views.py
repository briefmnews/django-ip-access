from django.http import HttpResponse
from django.views import View


class DummyView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Dummy class-based view response")
