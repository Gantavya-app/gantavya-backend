from django import forms
from .models import Photos, Landmark
from django.forms import ModelForm, TextInput

class PhotoUploadForm(ModelForm):
    class Meta:
        model = Photos
        fields = ['place', 'photo']

class LandmarkForm(ModelForm):
    class Meta:
        model = Landmark
        fields = ['name', 'address', 'type', 'description']
        widgets = {
            'name': TextInput(attrs={'class': 'py-1 px-1 ml-auto rounded-sm my-2 border-2 border'}),
            'address': TextInput(attrs={'class':'py-1 px-1 ml-auto rounded-sm my-2 border-2 border'}),
            'type': TextInput(attrs={'class': 'py-1 px-1 ml-auto rounded-sm my-2 border-2 border'}),
            'description': TextInput(attrs={'class': 'py-1 px-1 ml-auto rounded-sm my-2 border-2 border'}),
        }