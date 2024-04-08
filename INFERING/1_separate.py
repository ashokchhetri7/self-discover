import json
import csv

# Step 1: Load the JSON data
with open("/hdd1/ashok/PROMPT/_DATASET/BIG-Bench-Hard/bbh/causal_judgement.json", "r") as file:
    data = json.load(file)

# Extract the examples from the JSON data
examples = data['examples']

# Create the test.csv file with only the inputs
with open('test.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['input'])  # Write the header
    for example in examples:
        writer.writerow([example['input']])

# Create the org.csv file with inputs and targets
with open('org.csv', 'w', newline='', encoding='utf-8') as file:
    fieldnames = ['input', 'target']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for example in examples:
        writer.writerow({'input': example['input'], 'target': example['target']})