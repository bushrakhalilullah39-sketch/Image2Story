import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from backend.device import get_device
from config.settings import CAPTION_MODEL_NAME

class CaptionGenerator:
    def __init__(self):
        self.device = get_device()
        self.processor = BlipProcessor.from_pretrained(CAPTION_MODEL_NAME)
        self.model = BlipForConditionalGeneration.from_pretrained(CAPTION_MODEL_NAME)
        self.model.to(self.device)

    def generate_caption(self, image):
        inputs = self.processor(image, return_tensors="pt").to(self.device)
        with torch.no_grad():
            output = self.model.generate(**inputs)
        return self.processor.decode(output[0], skip_special_tokens=True)