import gradio as gr
from gradio import Interface
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

# Created by Gaurang Shukla

# Load model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Define Function
def generate_caption(image):
    inputs = processor(images=image, return_tensors="pt")
    output = model.generate(**inputs)
    return processor.batch_decode(output, skip_special_tokens=True)[0]

title = "✨ Gaurang Shukla ✨"
desc = "🎨 If this inspires you, let others know!"
long_desc = "🌟 Enjoyed this? spread the word! "
# Create Gradio Interface
gr.Interface(generate_caption,"image","text", theme=gr.themes.Glass(),
              title=title, description=desc, article=long_desc).launch(share=True)
