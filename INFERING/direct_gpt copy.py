import os
import csv
import json
from openai import OpenAI
from dotenv import load_dotenv
from tqdm import tqdm

# Load the API key from the .env file
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Function to read the JSON file
def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Function to send inputs to GPT-3.5-turbo and get the outputs
def generate_outputs(input_texts):
    responses = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an AI assistant."},
            {"role": "user", "content": '\n'.join(input_texts)}
        ]
    )
    return [response.message.content for response in responses.choices]

def main():
    # Load data from boolean_expressions.json
    data = read_json("/hdd1/ashok/PROMPT/_DATASET/BIG-Bench-Hard/bbh/boolean_expressions.json")
    inputs = [example["input"] for example in data["examples"]]
    targets = [example["target"] for example in data["examples"]]

    # Open CSV for appending predictions (avoid overwriting)
    csv_path = "boolean_expressions.csv"
    with open(csv_path, 'a', newline='') as csvfile:
        fieldnames = ['input', 'target', 'prediction']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Only write header if the file is new/empty
        if os.stat(csv_path).st_size == 0:
            writer.writeheader()

        batch_size = 10
        pbar = tqdm(total=50, desc="Processing inputs")  # Only process 50 samples
        for i in range(0, 50, batch_size):
            batch_inputs = inputs[i:i+batch_size]
            batch_outputs = generate_outputs(batch_inputs)
            for inp, tgt, pred in zip(batch_inputs, targets[i:i+batch_size], batch_outputs):
                writer.writerow({'input': inp, 'target': tgt, 'prediction': pred})
            pbar.update(len(batch_inputs))
        pbar.close()

if __name__ == "__main__":
    main()