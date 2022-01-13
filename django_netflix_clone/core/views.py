from typing import Dict, List
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

# Create your views here.


class Index(View):
    def get(self, request: HttpRequest, *args: List, **kwargs: Dict) -> HttpResponse:
        return render(request=request, template_name='index.html')
