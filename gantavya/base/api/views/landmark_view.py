from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import redirect, get_object_or_404

from base.serializers import LandmarkSerializer, PhotoSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from base.models import Landmark, Photos
from PIL import Image
from base.inference import predict




names= {0: 'airport', 1: 'bindabasini', 2: 'hemja', 3: 'museum', 4: 'pumdikot', 5: 'ramghat_gumba', 6: 'ric', 7: 'stupa'}

landmark_id = {0:"PEMA TS'AL Monastery (Hemja Gumba)", 1:"RIC Building, Pashchimanchal Campus", 2:'Pokhara International Airport', 3:"Ramghat Monastery", 4:"Peace Pagoda Stupa", 5:"Pumdikot Shiva Temple", 6:"Gorkha Museum", 7:"Bindabasini Temple" }

#map names to landmark_id
mapping = {0:3, 1:8, 2:1, 3:7, 4:6, 5:4, 6:2, 7:5}



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
def upload_photo_api(request, landmark_id):
    landmark = get_object_or_404(Landmark, pk=landmark_id)
    serializer = PhotoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(place=landmark)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)




# # get detail of landmark with key
# @api_view(['GET','POST'])
# def landmark_detail(request, landmark_id):
#     landmark = get_object_or_404(Landmark, pk=landmark_id)
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
def landmark_detail_api(request, landmark_id):
    landmark = get_object_or_404(Landmark, pk=landmark_id)
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
def delete_photo_api(request, photo_id):
    photo = get_object_or_404(Photos, pk=photo_id)
    landmark_id = photo.place.id

    # Delete the photo file from the filesystem
    photo.photo.delete()

    # Delete the Photo instance from the database
    photo.delete()

    return Response(status=204)  # No content response




@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_landmark_api(request):
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
def landmark_list_api(request):
    landmarks = Landmark.objects.all()
    serialized_landmarks = LandmarkSerializer(landmarks, many=True).data
    return Response(serialized_landmarks)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def prediction_api(request):
    image = request.FILES.get('image')
    predicted_class, confidence_score = predict(image)

    id_landmark = mapping[int(predicted_class)]
    landmark = get_object_or_404(Landmark, pk=id_landmark)
    photos = landmark.photos.all()[:2]

    data = {
        'predicted_class': predicted_class,
        'confidence_score': confidence_score,
        'landmark': LandmarkSerializer(landmark).data,
        'photos': [photo.image.url for photo in photos]
    }

    return Response(data)
