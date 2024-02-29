from ultralytics import YOLO
from PIL import Image
from rest_framework.exceptions import ValidationError
# from torchvision import transforms

model = YOLO('yolo.pt')

def predict(image_path, model=model):
    # Load and preprocess the image
    # try:
    image = Image.open(image_path)
    # transform = transforms.Compose([transforms.ToTensor()])
    # input_image = transform(image).unsqueeze(0)

    # Perform inference using the YOLO model
    results = model(image)
    # print("\n\nResults:", results[0])
    # print("BOXES:", prediction.boxes)
    # print("\n\n")

    # Extract the predicted class and confidence score (modify based on your model's output structure)
    if results:
        prediction = results[0]
        confidence_score = prediction.boxes.conf
        predicted_class = prediction.boxes.cls

        print(f"\n\n\n\n\n  Class: {predicted_class.item()} Score: {confidence_score.item()}\n\n\n\n\n\n")
        return (predicted_class.item(), confidence_score.item())
    else:
        return None, None
        
    # except ValidationError as e:
    #     error_message = str(e)
    #     return Response({"detail": error_message.strip("[]").strip("'")}, status=status.HTTP_400_BAD_REQUEST)