import gradio as gr
from transformers import pipeline

generator = pipeline("text-generation", model="gpt2")

def generateText(sample_text):
    result = generator(sample_text, max_length=50, num_return_sequences=1)
    final_output = result[0]["generated_text"]
    return final_output

title = "✨ Gaurang Shukla ✨"
desc = "🎨 If this inspires you, let others know!"
long_desc = "🌟 Enjoyed this? spread the word! "
# Create Gradio Interface

gr.Interface(generateText,"text","text", theme=gr.themes.Glass(),
              title=title, description=desc, article=long_desc).launch(share=True)