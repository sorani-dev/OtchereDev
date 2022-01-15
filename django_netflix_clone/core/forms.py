from django.forms import ModelForm
from .models import Profile


class ProfileForm(ModelForm):
    """Form definition for Profile."""

    class Meta:
        """Meta definition for Profileform."""

        model = Profile
        exclude = ['uuid']
