from django.shortcuts import render, redirect, get_object_or_404
from .forms import PhotoUploadForm, LandmarkForm
from .models import Landmark, Photos
from .inference import predict
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser



model_idx = {
    0: "Pokhara International Airport",
    1: "Bindabasini Temple",
    2: "Bouddha Stupa",
    3: "Pema T'SAL Monastery",
    4: "Mountain Museum",
    5: "Gurkha Memorial Museum",
    6: "Pulchowk ICTC Building",
    7: "Pumdikot Shiva Statue",
    8: "Ramghat Monastery",
    9: "WRC RIC Building",
    10: "Peace Stupa",
    11: "Thapathali Building",
    12: "Tribhuvan International Airport",
}

landmark_idx = {
    1: "Pokhara International Airport",
    2: "Peace Stupa",
    3: "Gurkha Memorial Museum",
    4: "Pumdikot Shiva Statue",
    5: "IOE, Pulchowk Campus (ICTC Building)",
    6: "Ramghat Gumba",
    7: "Pema TS'AL Monastery / Monastic Institute",
    8: "Bindhyabasini Temple",
    9: "IOE, Pashchimanchal Campus (RIC Building)",
    10: "	IOE, Thapathali Campus",
    11: "International Mountain Museum",
    12: "Bouddhanath Stupa",
    13: "Tribhuvan International Airport",
}


mapping = {
    0: 1,
    1: 8,
    2: 12,
    3: 7,
    4: 11,
    5: 3,
    6: 5,
    7: 4,
    8: 6,
    9: 9,
    10: 2,
    11: 10,
    12: 13,
}


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
        photo = landmark.photos.all()[:3]
        photos[landmark.id] = photo
    # photos = {'1':[image_1, image_2], '2':[image_1, image_2]}
    # print("Photos",photos)
    
    return render(request, 'base/Home.html', {'landmarks':all_landmarks, 'photos':photos})





def prediction_view(request):
    if request.method == 'POST':
        try:
            image = request.FILES.get('image')  # Assuming you have a form with a file input named 'image'

            # Perform prediction using the inference function
            predicted_class, confidence_score = predict(image)
            # print("Function call",predicted_class, confidence_score)
            message1 = f"CALL class: {predicted_class} score:{confidence_score}"



            id_landmark = mapping[int(predicted_class)]
            
            landmark = get_object_or_404(Landmark, pk=id_landmark)
            photos = landmark.photos.all()[:3]

            message2= f" id {id_landmark}"

            message3 = f"OUT class: {predicted_class} score:{confidence_score} landmark {landmark} photos{photos}"

            context = {'predicted_class':predicted_class, 'confidence_score': confidence_score, 'landmark':landmark, 'photos':photos, "message1":message1,"message2":message2, "message3":message3}
            # Pass the prediction results to the template
            
            return render(request, 'base/predict.html',  context)
        
        except Exception as e:
            error_message = str(e)
            context = {}
            if error_message == "a Tensor with 0 elements cannot be converted to Scalar":
                error_message = "Couldn't Predict For Given Image."
                context = {'message1':"Exception class no prediction"}
            
            return render(request, 'base/predict.html',  context)
            
    return render(request, 'base/predict.html')