from typing import Dict, List, Union

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from .forms import ProfileForm
from .models import Movie, Profile, Video

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


@method_decorator(login_required, name='dispatch')
class Watch(View):
    def get(self, request: HttpRequest, profile_id: str, *args: List, **kwargs: Dict) -> HttpResponse:
        try:
            profile: Profile = Profile.objects.get(uuid=profile_id)
            movies: QuerySet[Movie] = Movie.objects.filter(
                age_limit=profile.age_limit)

            if profile not in request.user.profiles.all():
                return redirect(to='core:profile_list')

            return render(request, 'movieList.html', {
                'movies': movies,
            })
        except Profile.DoesNotExist as e:
            return redirect(to='core:profile_list')


@method_decorator(login_required, name='dispatch')
class ShowMovieDetail(View):
    def get(self, request: HttpRequest, movie_id: str, *args: List, **kwargs: Dict) -> HttpResponse:
        try:
            movie: Movie = Movie.objects.get(uuid=movie_id)
            return render(request, 'movieDetail.html', {
                'movie': movie,
            })
        except Movie.DoesNotExist as e:
            return redirect(to='core:profile_list')


@method_decorator(login_required, name='dispatch')
class ShowMovie(View):
    def get(self, request: HttpRequest, movie_id: str, *args: List, **kwargs: Dict) -> HttpResponse:
        try:
            movie: Movie = Movie.objects.get(uuid=movie_id)
            videos: QuerySet[Video] = movie.videos.values()

            # Videos List
            videos_list: List[Video] = list(videos)

            # Get the episode number from the query parameters
            try:
                # Convert the episode number to int
                videoParams: int = int(request.GET.get('epi', 0))
                # Video is not in the video list
                if videoParams >= len(videos_list) or videoParams < 0:
                    raise IndexError(
                        f'Episode number (epi) must be in the range of the current videos registered: 0 to {len(videos_list)-1}, query params for epi was: {videoParams}')
            except (ValueError, IndexError) as e:
                print('error', e)
                videoParams = 0

            # The selected video url
            media_url: str = f"{settings.MEDIA_URL}{videos_list[videoParams]['file']}"

            return render(request=request, template_name='showMovie.html', context={
                'movie': videos_list,
                'media_url': media_url,
            })
        except Movie.DoesNotExist:
            return redirect(to='core:profile_list')
