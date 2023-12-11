from django.shortcuts import render, redirect, get_object_or_404
from .forms import PhotoUploadForm, LandmarkForm
from .models import Landmark, Photos
from PIL import Image



def upload_photo(request, landmark_id):
    landmark = get_object_or_404(Landmark, pk=landmark_id)

    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.place = landmark
            photo.save()
            return redirect('landmark_detail', landmark_id=landmark.id)
    else:
        form = PhotoUploadForm()

    return render(request, 'base/upload_photo.html', {'form': form, 'landmark': landmark})



def landmark_detail(request, landmark_id):
    landmark = get_object_or_404(Landmark, pk=landmark_id)
    photos = landmark.photos.all()  # Access all photos associated with the landmark

    if request.method == 'POST':
        photo_form = PhotoUploadForm(request.POST, request.FILES)
        if photo_form.is_valid():
            photo = photo_form.save(commit=False)
            photo.place = landmark

            photo.save()
            return redirect('landmark_detail', landmark_id=landmark.id)
    else:
        photo_form = PhotoUploadForm()

    return render(request, 'base/landmark_detail.html', {'landmark': landmark, 'photos': photos, 'photo_form': photo_form})



def delete_photo(request, photo_id):
    photo = get_object_or_404(Photos, pk=photo_id)
    landmark_id = photo.place.id

    # Delete the photo file from the filesystem
    photo.photo.delete()

    # Delete the Photo instance from the database
    photo.delete()

    return redirect('landmark_detail', landmark_id=landmark_id)


def create_landmark(request):
    if request.method == 'POST':
        form = LandmarkForm(request.POST)
        if form.is_valid():
            landmark = form.save()
            return redirect('landmark_detail', landmark_id=landmark.id)
    else:
        form = LandmarkForm()

    return render(request, 'base/create_landmark.html', {'form': form})



# def landmark_list(request):
