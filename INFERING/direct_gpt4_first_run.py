import os
import csv
import json
from openai import OpenAI
from dotenv import load_dotenv
from tqdm import tqdm

# Load the API key from the .env file
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Function to send inputs to GPT-3.5-turbo and get the outputs
def generate_outputs(input_texts):
    responses = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an AI assistant. Don't give question numbers, just give one-word answers for each row. True or False Only. No more comments or any asking"},
            {"role": "user", "content": '\n'.join(input_texts)}
        ]
    )
    return [response.message.content for response in responses.choices]

def main():
    data_path = "/hdd1/ashok/PROMPT/_DATASET/BIG-Bench-Hard/bbh/boolean_expressions.json"
    csv_path = "/hdd1/ashok/PROMPT/_DATASET/BIG-Bench-Hard/bbh/be.csv"

    # Load data from causal_judgement.json
    with open(data_path, 'r') as file:
        data = json.load(file)
    inputs = [example["input"] for example in data["examples"]]

    # Open CSV for appending predictions
    with open(csv_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)

        batch_size = 10
        pbar = tqdm(total=len(inputs), desc="Processing inputs")
        max_batches = 200  # Set the maximum number of batches to process
        batch_count = 0
        for i in range(0, len(inputs), batch_size):
            if batch_count >= max_batches:
                break  # Stop processing after 2 batches

            batch_inputs = inputs[i:i+batch_size]
            batch_outputs = generate_outputs(batch_inputs)
            for pred in batch_outputs:
                if pred.strip():
                    writer.writerow([pred.strip()])
                else:
                    writer.writerow(["No_pred"])
            pbar.update(batch_size)
            batch_count += 1
        pbar.close()

if __name__ == "__main__":
    main()



# You are an AI assistant. Don't give question numbers, just give one-word answers for each row. True or False Only. No more comments or any asking