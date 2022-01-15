from typing import Dict, List, Union

from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from .forms import ProfileForm

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


@method_decorator(login_required, name='dispatch')
class CreateProfile(View):
    def get(self, request: HttpRequest, *args: List, **kwargs: Dict) -> HttpResponse:
        # Form for creating profile
        form = ProfileForm()

        return render(request, 'profileCreate.html', {
            'form': form,
        })

    def post(self, request: HttpRequest, *args: List, **kwargs: Dict) -> HttpResponse:
        form = ProfileForm(request.POST or None)

        if form.is_valid():
            profile: Union[Profile, None] = Profile.objects.create(
                **form.cleaned_data)
            if profile:
                request.user.profiles.add(profile)
                return redirect(to='core:profile_list')
            # print(form.cleaned_data)

        return render(request, 'profileCreate.html', {
            'form': form,
        })
