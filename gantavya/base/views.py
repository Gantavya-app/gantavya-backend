from django.shortcuts import render, redirect, get_object_or_404
from .forms import PhotoUploadForm, LandmarkForm
from .models import Landmark, Photos
from .inference import predict
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser


names= {0: 'airport', 1: 'bindabasini', 2: 'hemja', 3: 'museum', 4: 'pumdikot', 5: 'ramghat_gumba', 6: 'ric', 7: 'stupa'}

landmark_id = {0:"PEMA TS'AL Monastery (Hemja Gumba)", 1:"RIC Building, Pashchimanchal Campus", 2:'Pokhara International Airport', 3:"Ramghat Monastery", 4:"Peace Pagoda Stupa", 5:"Pumdikot Shiva Temple", 6:"Gorkha Museum", 7:"Bindabasini Temple" }

#map names to landmark_id
mapping = {0:3, 1:8, 2:1, 3:7, 4:6, 5:4, 6:2, 7:5}


@permission_classes([IsAdminUser])
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


@permission_classes([IsAdminUser])
def delete_photo(request, photo_id):
    photo = get_object_or_404(Photos, pk=photo_id)
    landmark_id = photo.place.id

    # Delete the photo file from the filesystem
    photo.photo.delete()

    # Delete the Photo instance from the database
    photo.delete()

    return redirect('landmark_detail', landmark_id=landmark_id)


@permission_classes([IsAdminUser])
def create_landmark(request):
    if request.method == 'POST':
        form = LandmarkForm(request.POST)
        if form.is_valid():
            landmark = form.save()
            return redirect('landmark_detail', landmark_id=landmark.id)
    else:
        form = LandmarkForm()

    return render(request, 'base/create_landmark.html', {'form': form})



def landmark_list(request):
    all_landmarks = Landmark.objects.all()
    photos = {}
    for landmark in all_landmarks:
        photo = landmark.photos.all()[:2]
        photos[landmark.id] = photo
    # photos = {'1':[image_1, image_2], '2':[image_1, image_2]}
    # print("Photos",photos)
    
    return render(request, 'base/Home.html', {'landmarks':all_landmarks, 'photos':photos})





def prediction_view(request):
    if request.method == 'POST':
        image = request.FILES.get('image')  # Assuming you have a form with a file input named 'image'

        # Perform prediction using the inference function
        predicted_class, confidence_score = predict(image)
        # print("Function call",predicted_class, confidence_score)
        message1 = f"CALL class: {predicted_class} score:{confidence_score}"



        id_landmark = mapping[int(predicted_class)]
        
        landmark = get_object_or_404(Landmark, pk=id_landmark)
        photos = landmark.photos.all()[:2]

        message2= f" id {id_landmark}"

        message3 = f"OUT class: {predicted_class} score:{confidence_score} landmark {landmark} photos{photos}"

        context = {'predicted_class':predicted_class, 'confidence_score': confidence_score, 'landmark':landmark, 'photos':photos, "message1":message1,"message2":message2, "message3":message3}
        # Pass the prediction results to the template
        
        return render(request, 'base/predict.html',  context)
    return render(request, 'base/predict.html')