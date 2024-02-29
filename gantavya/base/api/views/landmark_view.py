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

import base64
from django.core.files.base import ContentFile





model_idx = {0:'Pokhara International Airport', 1:'Bindabasini Temple', 2:'Bouddha Stupa', 3:"Pema T'SAL Monastery", 4:'Mountain Museum', 5:'Gurkha Memorial Museum', 6:'Pulchowk ICTC Building', 7:'Pumdikot Shiva Statue', 8:'Ramghat Monastery', 9:'WRC RIC Building', 10:'Peace Stupa', 11:'Thapathali Building',12:"Tribhuvan International Airport" }

landmark_idx = {1:'Pokhara International Airport', 2:"Peace Stupa", 3:"Gurkha Memorial Museum", 4:"Pumdikot Shiva Statue", 5:"IOE, Pulchowk Campus (ICTC Building)", 6:"Ramghat Gumba", 7:"Pema TS'AL Monastery / Monastic Institute", 8:"Bindhyabasini Temple", 9:"IOE, Pashchimanchal Campus (RIC Building)", 10:"	IOE, Thapathali Campus", 11:"International Mountain Museum", 12:"Bouddhanath Stupa", 13:"Tribhuvan International Airport",  }


mapping = {0:1, 1:8, 2:12, 3:7, 4:11, 5:3, 6:5, 7:4, 8:6, 9:9, 10:2, 11:10, 12:13}


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
        photos = landmark.photos.all()[:3]
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
        image_data = request.data.get('image')  # Assuming 'image' is the key for base64-encoded image data
        if not image_data:
            return ValidationError("No Image Data Provided")
        
        # print(image_data)
        
        # Decode base64 data
        decoded_image_data = base64.b64decode(image_data)
        
        # Save decoded image data to a temporary file
        temp_image = ContentFile(decoded_image_data, name='temp_image.jpg')  # Change 'temp_image.jpg' as needed
        predicted_class, confidence_score = predict(temp_image)

        # print("VIEWS: ", predicted_class, confidence_score, mapping[int(predicted_class)])
        
        # Now you can use temp_image like any other file uploaded through Django's file input
        landmark = get_object_or_404(Landmark, id=mapping[int(predicted_class)])
        photos = landmark.photos.all()

        if landmark:
            landmark.pred_history.add(request.user)
   
        data = {
            'predicted_class': predicted_class,
            'confidence_score': confidence_score,
            'landmark': LandmarkSerializer(landmark).data,
            'photos': PhotoSerializer(photos, many=True).data,
        }

        return Response(data)
    
    except ValidationError as e:
        error_message = str(e)
        return Response({"detail": error_message.strip("[]").strip("'")}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        error_message = str(e)
        if error_message == "a Tensor with 0 elements cannot be converted to Scalar":
            error_message = "Couldn't Predict For Given Image."
        return Response({"detail": error_message.strip("[]").strip("'")}, status=status.HTTP_400_BAD_REQUEST)
    
    




@api_view(["POST"])
@permission_classes([IsAuthenticated])
def save_landmark(request, pk):
    if request.method == 'POST':
        try:
            if request.data.get('value'):
                value = request.data.get('value')
            else: 
                raise ValidationError("No value was sent")
            
            landmark = get_object_or_404(Landmark, id=pk)
            user = request.user

            if value=='False' or value=='false' or value==False:
                landmark.saved_by.remove(user)
                return Response({'detail':"Unsaved Landmark"})
            else:
                landmark.saved_by.add(user)
                return Response({'detail':"Saved Landmark"})

        except ValidationError as e:
            error_message = str(e)
            return Response({"detail": error_message.strip("[]").strip("'")}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            error_message = str(e)
            return Response({"detail": error_message.strip("[]").strip("'")}, status=status.HTTP_400_BAD_REQUEST)       
        


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def saved_landmarks(request):
    try:
        user = request.user
        saved_landmarks  = user.saved_landmarks.all()

        # Serialize landmark data
        serializer = LandmarkSerializer(saved_landmarks, many=True)
        
        return Response(serializer.data)
    
    
    except Exception as e:
            error_message = str(e)
            return Response({"detail": error_message.strip("[]").strip("'")}, status=status.HTTP_400_BAD_REQUEST) 
    


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_prediction_history(request):
    try:
        user = request.user
        predicted_landmarks = user.predicted_landmarks.all()
        
        # Serialize landmark data
        serializer = LandmarkSerializer(predicted_landmarks, many=True)
        
        return Response(serializer.data)
    
    except Exception as e:
            error_message = str(e)
            return Response({"detail": error_message.strip("[]").strip("'")}, status=status.HTTP_400_BAD_REQUEST) 