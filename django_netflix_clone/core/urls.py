import imp
from django.urls import path

from .views import CreateProfile, Index, ProfileList, Watch

app_name = 'core'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('profile/', ProfileList.as_view(), name='profile_list'),
    path('profile/create/', CreateProfile.as_view(), name='profile_create'),
    path('watch/<str:profile_id>/', Watch.as_view(), name='watch')
]
