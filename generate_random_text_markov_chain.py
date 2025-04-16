import random

# Created by Gaurang Shukla
# based on given input text -> to generate random text using Markov Chain

def generate_text(corpus, length=100):
    """
    A basic text generation AI using a simple Markov chain model.

    Args:
        corpus (str): The text data to learn from.
        length (int): The desired length of the generated text (number of words).

    Returns:
        str: The generated text.
    """

    # 1. Tokenize the corpus (split into words)
    words = corpus.lower().split()

    if not words:
        return "Error: Empty corpus provided."

    # 2. Create a word-to-word transition dictionary (Markov chain)
    word_transitions = {}
    for i in range(len(words) - 1):
        current_word = words[i]
        next_word = words[i + 1]
        if current_word not in word_transitions:
            word_transitions[current_word] = []
        word_transitions[current_word].append(next_word)

    # 3. Choose a random starting word
    start_word = random.choice(words)
    generated_text = [start_word]

    # 4. Generate subsequent words based on the transitions
    for _ in range(length - 1):
        last_word = generated_text[-1]
        if last_word in word_transitions:
            next_word = random.choice(word_transitions[last_word])
            generated_text.append(next_word)
        else:
            # If the last word has no recorded transitions, stop generating
            break

    return " ".join(generated_text)

# Example usage:
if __name__ == "__main__":
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
    #sample_text = open('D:\wspython\AIGym\elephant.txt',encoding='utf-8').read()  
    
    generated_output = generate_text(sample_text, length=50)
    print("Generated Text:")
    print(generated_output)