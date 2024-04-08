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
        fieldnames = ['input', 'target']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for inp, tgt in zip(inputs, targets):
            writer.writerow({'input': inp, 'target': tgt})

def generate_outputs(input_texts):
    responses = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an AI assistant."},
            {"role": "user", "content": '\n'.join(input_texts)}
        ]
    )
    return [response.message.content for response in responses.choices]

def calculate_accuracy(predictions, targets):
    correct = 0
    total = len(predictions)
    for prediction, target in zip(predictions, targets):
        if prediction == target:
            correct += 1
    accuracy = (correct / total) * 100
    return accuracy

def main(create_csv_flag, call_gpt_flag, use_batch_flag):
    data = read_json("/hdd1/ashok/PROMPT/_DATASET/BIG-Bench-Hard/bbh/boolean_expressions.json")

    if create_csv_flag:
        create_csv(data, 'boolean_expressions_direct.csv')

    inputs = []
    targets = []
    with open('boolean_expressions.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            inputs.append(row['input'])
            # targets.append(row['target'])

    if call_gpt_flag:
        predictions = []
        if use_batch_flag:
            batch_size = 10
            pbar = tqdm(total=len(inputs), desc="Processing inputs")

            keep_running = True
            while keep_running:
                batch_inputs = inputs[:batch_size]
                inputs = inputs[batch_size:]

                batch_outputs = generate_outputs(batch_inputs)
                predictions.extend(batch_outputs)

                with open('boolean_expressions.csv', 'a', newline='') as csvfile:
                    fieldnames = ['input', 'target', 'prediction']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    for inp, tgt, pred in zip(batch_inputs, targets[:len(batch_inputs)], batch_outputs):
                        writer.writerow({'input': inp, 'target': tgt, 'prediction': pred})
                        targets.remove(tgt)

                pbar.update(batch_size)

                if not inputs:
                    keep_running = False
                    break

                user_input = input(f"Continue processing? (y/n) (Total inputs remaining: {len(inputs)}): ")
                if user_input.lower() != 'y':
                    keep_running = False

            pbar.close()

        else:
            outputs = generate_outputs(inputs)
            predictions = outputs

            with open('boolean_expressions.csv', 'a', newline='') as csvfile:
                fieldnames = ['input', 'target', 'prediction']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                for inp, tgt, pred in zip(inputs, targets, predictions):
                    writer.writerow({'input': inp, 'target': tgt, 'prediction': pred})

        accuracy = calculate_accuracy(predictions, targets)
        print(f"Accuracy: {accuracy:.2f}%")

if __name__ == "__main__":
    create_csv_flag = True
    call_gpt_flag = False
    use_batch_flag = False

    main(create_csv_flag, call_gpt_flag, use_batch_flag)