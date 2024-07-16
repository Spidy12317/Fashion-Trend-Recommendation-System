import os
import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from torch.nn.functional import cosine_similarity


def load_clip_model(model_path):
    model = CLIPModel.from_pretrained(model_path, local_files_only=True)
    processor = CLIPProcessor.from_pretrained(model_path, local_files_only=True)
    return model, processor

def get_text_embedding(model, processor, text):
    inputs = processor(text=[text], return_tensors="pt", padding=True)
    
    with torch.no_grad():
        text_features = model.get_text_features(**inputs)
    
    return text_features

def get_image_embedding(model, processor, image_path):
    image = Image.open(image_path)
    # image = image.resize((224, 224))
    inputs = processor(images=image, return_tensors="pt", padding=True)
    
    with torch.no_grad():
        image_features = model.get_image_features(**inputs)
    
    return image_features


def calculate_similarity(embedding1, embedding2):
    return cosine_similarity(embedding1, embedding2).item()

   