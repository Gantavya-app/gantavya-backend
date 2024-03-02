from ultralytics import YOLO
from PIL import Image
from rest_framework.exceptions import ValidationError
from pathlib import Path

# from torchvision import transforms
MODEL_PATH = Path(__file__).resolve().parent.parent

model = YOLO(MODEL_PATH / "yolo.pt")


def predict(image_path, model=model):
    # Load and preprocess the image
    # try:
    image = Image.open(image_path)
    # transform = transforms.Compose([transforms.ToTensor()])
    # input_image = transform(image).unsqueeze(0)

    # Perform inference using the YOLO model
    results = model(image)
    print("\n\nResults\n\n:", results)
    # print("BOXES:", prediction.boxes)
    # print("\n\n")

    # Extract the predicted class and confidence score (modify based on your model's output structure)
    if results:
        predictions = results[0]

        print("\nIF STATEMENT\n", predictions[0].boxes.cls)
        
        # Count occurrences of each class
        class_counts = {}
        for prediction in predictions:
            class_idx = int(prediction.boxes.cls)
            if class_idx in class_counts:
                class_counts[class_idx] += 1
            else:
                class_counts[class_idx] = 1

        print("\n\n class counts \n\n",class_counts)

        # Choose the class with the highest occurrence count
        most_common_class = max(class_counts, key=class_counts.get)

        print("\n\n most_common_class \n\n",most_common_class)



        # Find the first prediction for the most common class
        selected_prediction = None
        for prediction in predictions:
            if int(prediction.boxes.cls) == most_common_class:
                selected_prediction = prediction
                break
        
        if selected_prediction:
            confidence_score = selected_prediction.boxes.conf
            predicted_class = selected_prediction.boxes.cls
            print(f"\n\n\n\n\n  Class: {predicted_class.item()} Score: {confidence_score.item()}\n\n\n\n\n\n")
            return (predicted_class.item(), confidence_score.item())
        else:
            return None, None
    else:
        return None, None

