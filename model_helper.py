import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision import models

# Define class labels
class_labels = ['Front_Breakage', 'Front_Crushed', 'Front_Normal', 'Rear_Breakage', 'Rear_Crushed', 'Rear_Normal']  # Update if order is different

class CarClassifier_ResNet50(nn.Module):
    def __init__(self,num_classes):
        super().__init__()
        self.model=models.resnet50(weights='DEFAULT')

        for param in self.model.parameters():
            param.requires_grad=False

        for param in self.model.layer4.parameters():
            param.requires_grad=True

        self.model.fc=nn.Sequential(
            nn.Dropout(0.49225022231722876),
            nn.Linear(self.model.fc.in_features,num_classes)
        )
    def forward(self,x):
        return self.model(x)

trained_model=None
# is_trained=False


def predict(image_pil):
    # Preprocessing
    image_pil = image_pil.convert("RGB")
    
    transform = transforms.Compose([
        transforms.Resize((224, 224)),  # match training size
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],  # ImageNet mean
                            [0.229, 0.224, 0.225])   # ImageNet std
    ])

    image_tensor=transform(image_pil) # Apply the transforms
    image_tensor = image_tensor.unsqueeze(0)  # Add batch dim , updated  size=> [1,3,224,224]

    global trained_model
    # global is_trained

    if not trained_model:
        # is_trained=True
        trained_model=CarClassifier_ResNet50(6)
        trained_model.load_state_dict(torch.load("model/saved_model.pth"))
        trained_model.eval()

    # Run inference
    with torch.no_grad():
        outputs = trained_model(image_tensor)
        _, predicted = torch.max(outputs, 1)
        return class_labels[predicted.item()]
