
from transformers import pipeline

# Created by Gaurang Shukla
# based on given input text -> to generate random text using GPT2

generator = pipeline("text-generation", model="gpt2")

sample_text = """
    Elephants, the majestic creatures that roam the Earth, are the largest land animals
    Elephants are the largest animals on land.
    Elephants have huge bodies.
    They have wide legs like pillars.
    Elephants are grey in colour.
    Elephants have large floppy ears like fans.
    They have a large trunk.
    They grab food and suck water with their trunk.
    They can also lift heavy weights with the help of the trunk.
    Elephants tusks are teeth.
    Elephants are herbivores.
    """

#result = generator(sample_text, max_length=500, num_return_sequences=1)
result = generator("Futre of AI", max_length=50, num_return_sequences=1)
print("Final Output : ")
print(result[0]["generated_text"])


