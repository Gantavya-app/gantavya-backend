from django import forms
from .models import Photos, Landmark

class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Photos
        fields = ['place', 'photo']


class LandmarkForm(forms.ModelForm):
    class Meta:
        model = Landmark
        fields = ['name', 'address', 'type', 'description']