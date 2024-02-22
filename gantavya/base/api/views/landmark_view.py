from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import redirect, get_object_or_404

from base.serializers import LandmarkSerializer, PhotoSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import ValidationError
from rest_framework import status

from base.models import Landmark, Photos
from PIL import Image
from base.inference import predict





# model_idx = ['Pokhara International Airport', 'Bindabasini Temple', 'Bouddha Stupa', "Pema T'SAL Monastery", 'Mountain Museum', 'Gurkha Memorial Museum', 'Pulchowk ICTC Building', 'Pumdikot Shiva Statue', 'Ramghat Monastery', 'WRC RIC Building', 'Peace Stupa', 'Thapathali Building' ]

landmark_idx = {0:'Pokhara International Airport', 1:"Peace Stupa", 2:"Gurkha Memorial Museum", 3:"Pumdikot Shiva Statue", 4:"IOE, Pulchowk Campus (ICTC Building)", 5:"Ramghat Gumba", 6:"Pema TS'AL Monastery / Monastic Institute", 7:"Bindhyabasini Temple", 8:"IOE, Pashchimanchal Campus (RIC Building)", 9:"	IOE, Thapathali Campus", 10:"International Mountain Museum", 11:"Bouddhanath Stupa", 12:"Tribhuvan International Airport",  }


mapping = {}


# receive image from frontend and save it in backend media file and return status
# @api_view(['POST'])
# @permission_classes([IsAdminUser])
# def upload_photo(request, landmark_id):
#     landmark = get_object_or_404(Landmark, pk=landmark_id)
#     if request.method == 'POST':
#         image_data = request.FILES.get('image')
#         if image_data:
#             photo = Photos(image=image_data)
#             photo.place = landmark
#             photo.save()
#             return JsonResponse({'success': True, 'message': 'Photo uploaded successfully'})
#         else:
#             return JsonResponse({'success': False, 'message': 'No image data received'}, status=400)
#     return JsonResponse({'error': 'Method not allowed'}, status=405)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def upload_photo(request, pk):
    landmark = get_object_or_404(Landmark, id=pk)
    serializer = PhotoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(place=landmark)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)




# # get detail of landmark with key
# @api_view(['GET','POST'])
# def landmark_detail(request, pk):
#     landmark = get_object_or_404(Landmark, id=pk)
#     photos = landmark.photos.all()  # Access all photos associated with the landmark

#     if request.method == 'POST':
#         image_data = request.FILES.get('image')

#         if image_data:
#             photo = Photos(image=image_data)
#             photo.place = landmark
#             photo.save()

#             return JsonResponse({'success': True, 'message': 'Photo uploaded successfully'})
#         else:
#             return JsonResponse({'success': False, 'message': 'No image data received'}, status=400)

#     return JsonResponse({'error': 'Method not allowed'}, status=405)

@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def landmark_detail(request, pk):
    landmark = get_object_or_404(Landmark, id=pk)
    if request.method == 'POST':
        image_file = request.FILES.get('image')
        if image_file:
            photo = Photos.objects.create(place=landmark, image=image_file)
            serializer = PhotoSerializer(photo)
            return Response(serializer.data, status=201)
        return Response({'error': 'No image file provided.'}, status=400)
    else:
        photos = landmark.photos.all()
        landmark_serializer = LandmarkSerializer(landmark)
        return Response({'landmark': landmark_serializer.data, 'photos': PhotoSerializer(photos, many=True).data})


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_photo(request, pk):
    photo = get_object_or_404(Photos, id=pk)
    landmark_id = photo.place.id

    # Delete the photo file from the filesystem
    photo.photo.delete()

    # Delete the Photo instance from the database
    photo.delete()

    return Response(status=204)  # No content response




@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_landmark(request):
    if request.method == 'POST':
        name = request.data.get('name')  # Assuming 'name' is the only field required
        if name:
            landmark = Landmark.objects.create(name=name)
            serializer = LandmarkSerializer(landmark)
            return Response(serializer.data, status=201)
        return Response({'error': 'Name field is required.'}, status=400)
    



# List all landmarks for homepage
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def landmark_list(request):
    landmarks = Landmark.objects.all()
    serialized_landmarks = LandmarkSerializer(landmarks, many=True).data
    return Response(serialized_landmarks)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def prediction(request):
    try:
        image = request.FILES.get('image')
        predicted_class, confidence_score = predict(image)

        id_landmark = mapping.get(int(predicted_class))
        if id_landmark is None:
            raise ValidationError("Invalid predicted class")
        
        
        landmark = get_object_or_404(Landmark, id=id_landmark)
        photos = landmark.photos.all()[:2]

        if landmark:
            landmark.pred_history.add(request.user)
   
        data = {
            'predicted_class': predicted_class,
            'confidence_score': confidence_score,
            'landmark': LandmarkSerializer(landmark).data,
            'photos': [photo.image.url for photo in photos]
        }

        return Response(data)

    except Exception as e:
        return Response({"detail": error_message.strip("[]").strip("'")}, status=status.HTTP_400_BAD_REQUEST)
    
    except ValidationError as e:
        error_message = str(e)
        return Response({"detail": error_message.strip("[]").strip("'")}, status=status.HTTP_400_BAD_REQUEST)





def save_landmark(request):
    if request.method == 'POST' and request.is_ajax():
        landmark_id = request.POST.get('landmark_id')
        is_checked = request.POST.get('is_checked')

        landmark = Landmark.objects.get(id=landmark_id)
        user = request.user

        if is_checked == 'true':
            landmark.saved_by.add(user)
        else:
            landmark.saved_by.remove(user)

        return Response({'success': True})
    else:
        return Response({'success': False})