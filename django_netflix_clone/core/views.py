from typing import Dict, List

from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from .models import Profile

# Create your views here.


class Index(View):
    def get(self, request: HttpRequest, *args: List, **kwargs: Dict) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect(to='core:profile_list')
        return render(request=request, template_name='index.html')


@method_decorator(login_required, name='dispatch')
class ProfileList(View):
    def get(self, request: HttpRequest, *args: List, **kwargs: Dict) -> HttpResponse:
        profiles: QuerySet[Profile] = request.user.profiles.all()
        return render(request, 'profileList.html', {
            'profiles': profiles
        })
