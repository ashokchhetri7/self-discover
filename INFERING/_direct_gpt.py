import os
import csv
import json
from openai import OpenAI
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def create_csv(json_data, csv_file):
    inputs = [example["input"] for example in json_data["examples"]]
    targets = [example["target"] for example in json_data["examples"]]
    with open(csv_file, 'w', newline='') as csvfile:
        fieldnames = ['input', 'target', 'prediction']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for inp, tgt in zip(inputs, targets):
            writer.writerow({'input': inp, 'target': tgt})

def generate_outputs(input_texts, batch_size=10):
    all_outputs = []
    for i in tqdm(range(0, len(input_texts), batch_size), desc="Processing batches"):
        batch = input_texts[i:i+batch_size]
        responses = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI assistant."},
                {"role": "user", "content": "Your primary task is to review a series of questions and select the most appropriate answer choice from the given options (A, B, C, D, E, or F) for each. When you encounter a question where the date or timing is unclear or not understood, respond with '(X)' to indicate this specific issue. For all other questions, select the answer choice that best fits the information provided, and format your response by enclosing it in parentheses e.g. (A). Ensure your answers are listed in order, corresponding to the sequence of questions asked, and include only the answer choices in your response, with no additional text or explanations.\n".join(batch)}
            ]
        )
        batch_outputs = [response.message.content.strip().split() for response in responses.choices]
        print(f"Batch outputs: {batch_outputs}")
        all_outputs.extend(batch_outputs)
    return all_outputs

def save_predictions_to_csv(csv_file):
    inputs = []
    targets = []
    with open(csv_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames
        if 'prediction' not in fieldnames:
            fieldnames.append('prediction')
        for row in reader:
            inputs.append(row['input'])
            targets.append(row['target'])

    all_predictions = generate_outputs(inputs, batch_size=10)

    with open(csv_file, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for inp, tgt, batch_preds in zip(inputs, targets, all_predictions):
            for i, pred in enumerate(batch_preds):
                if i >= len(batch_preds):
                    pred = ''
                writer.writerow({'input': inp, 'target': tgt, 'prediction': pred})

def calculate_accuracy(targets, predictions):
    correct = 0
    for tgt, pred in zip(targets, predictions):
        if tgt == pred:
            correct += 1
    accuracy = correct / len(targets)
    return accuracy

# Read JSON data
data = read_json("/hdd1/ashok/PROMPT/_DATASET/BIG-Bench-Hard/bbh/causal_judgement.json")

# Create CSV from JSON data
create_csv(data, "predictions.csv")

# Save predictions to the CSV file
save_predictions_to_csv("predictions.csv")

# Calculate and print accuracy
inputs = []
targets = []
predictions = []
with open("predictions.csv", 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        inputs.append(row['input'])
        targets.append(row['target'])
        predictions.append(row['prediction'])

accuracy = calculate_accuracy(targets, predictions)
print(f"\nAccuracy: {accuracy * 100:.2f}%")



# Boolean exp
#You will give just give one-word answers (True or False Only) for each row. Do not write any further comments
#You are an AI assistant. Your task is to read a series of questions and select the most appropriate answer choice from the given options (A, B, C, D, E, or F) for each one. You must format your response by enclosing your answer choice in parentheses and including the question number followed by a period and a space before the answer, like this: '1. (A)'. Do not include any additional text, explanations, or content outside of this format.
# Your primary task is to review a series of questions and select the most appropriate answer choice from the given options (A, B, C, D, E, or F) for each. When you encounter a question where the date or timing is unclear or not understood, respond with '(X)' to indicate this specific issue. For all other questions, select the answer choice that best fits the information provided, and format your response by enclosing it in parentheses e.g. (A). Ensure your answers are listed in order, corresponding to the sequence of questions asked, and include only the answer choices in your response, with no additional text or explanations.

