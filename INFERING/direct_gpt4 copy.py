import openai
import json
import os
from dotenv import load_dotenv

# Load the API key from the .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set your OpenAI API key here
api_key = OPENAI_API_KEY


# Function to read JSON file
def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Function to send input to GPT-4 and get the generated output
def generate_output(input_text):
    openai.api_key = api_key
    response = openai.Completion.create(
        engine="text-davinci-004",
        prompt=input_text,
        max_tokens=50
    )
    return response.choices[0].text.strip()

# Function to calculate accuracy
def calculate_accuracy(predictions, targets):
    correct = 0
    total = len(predictions)
    for prediction, target in zip(predictions, targets):
        if prediction == target:
            correct += 1
    accuracy = (correct / total) * 100
    return accuracy

# Main function
def main():
    # Load data from boolean_expressions.json
    data = read_json("/hdd1/ashok/PROMPT/_DATASET/BIG-Bench-Hard/bbh/boolean_expressions.json")
    inputs = [example["input"] for example in data["examples"]]
    targets = [example["target"] for example in data["examples"]]

    # Generate predictions using GPT-4
    predictions = [generate_output(input_text) for input_text in inputs]

    # Calculate accuracy
    accuracy = calculate_accuracy(predictions, targets)
    print(f"Accuracy: {accuracy:.2f}%")

if __name__ == "__main__":
    main()
