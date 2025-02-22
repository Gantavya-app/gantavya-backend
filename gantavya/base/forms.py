from django import forms
from .models import Photos, Landmark
from django.forms import ModelForm, TextInput, Select, FileInput

class PhotoUploadForm(ModelForm):
    class Meta:
        model = Photos
        fields = ['place', 'photo']
        widgets = {
            'place': Select(attrs={'class': 'py-1 px-1 ml-auto rounded-sm my-2 border-2 border bg-white w-[260px]'}),
            'photo': FileInput(attrs={'class': 'py-0.5 px-1 ml-auto rounded-sm my-2 border-2 border w-[260px]'}),
        }

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