import os
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

def generate_outputs(input_data, batch_size=10):
    inputs = [example["input"] for example in input_data["examples"]]
    targets = [example["target"] for example in input_data["examples"]]
    all_outputs = []
    for i in tqdm(range(0, len(inputs), batch_size), desc="Processing batches"):
        batch_inputs = inputs[i:i+batch_size]
        batch_targets = targets[i:i+batch_size]
        prompt = "Evaluate the result of a random Boolean expression.\n\n"
        for inp, tgt in zip(batch_inputs, batch_targets):
            prompt += f"Q: {inp}\nA: {tgt}\n\n"
        prompt += "Q: "
        responses = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        batch_outputs = [response.message.content.strip() for response in responses.choices]
        for j, pred in enumerate(batch_outputs):
            output = {
                "input": prompt,
                "prediction": pred,
                "target": batch_targets[j]
            }
            all_outputs.append(output)
    return all_outputs

def save_outputs_to_json(input_data, output_data, output_file):
    output_dict = {
        "canary": input_data["canary"],
        "outputs": output_data
    }
    with open(output_file, 'w') as file:
        json.dump(output_dict, file, indent=2)

# Read JSON data
input_data = read_json("/hdd1/ashok/PROMPT/_DATASET/BIG-Bench-Hard/bbh/boolean_expressions.json")

# Generate outputs using OpenAI GPT-3.5 Turbo
output_data = generate_outputs(input_data, batch_size=10)

# Save outputs to JSON file
save_outputs_to_json(input_data, output_data, "output.json")