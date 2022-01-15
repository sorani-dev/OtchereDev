import imp
from django.urls import path

from .views import Index, ProfileList

app_name = 'core'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('profile/', ProfileList.as_view(), name='profile_list'),
]
