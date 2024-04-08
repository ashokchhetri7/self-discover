# import pandas as pd


# csv_file_path1 = '/hdd1/ashok/PROMPT/SELF-DISCOVER/org.csv'
# csv_file_path2 = '/hdd1/ashok/PROMPT/SELF-DISCOVER/updated_test.csv'


# data1 = pd.read_csv(csv_file_path1)
# data2 = pd.read_csv(csv_file_path2)

# selected_columns_data1 = data1[['input', 'target']]
# selected_columns_data2 = data2[['input', 'predicted']]


# merged_columns = pd.concat([selected_columns_data1, selected_columns_data2], axis=1)

# output_file_path = 'Compare.csv'
# merged_columns.to_csv(output_file_path, index=False)

# print(f'Selected columns saved to {output_file_path}')



# # #Prediction
# # # Load the CSV file
# # csv_file_path = 'Compare.csv'
# # df = pd.read_csv(csv_file_path)

# df = merged_columns

# # Assuming the CSV file has columns named 'target' and 'predicted'
# # Calculate the accuracy
# accuracy = (df['target'] == df['predicted']).mean()

# print(f'Accuracy: {accuracy:.3f}')



# #Given the input from the excel, predict the output for each row, Only predict one word. and save it in the predicted column



import pandas as pd
import re

csv_file_path1 = '/hdd1/ashok/PROMPT/SELF-DISCOVER/org.csv'
csv_file_path2 = '/hdd1/ashok/PROMPT/_DATASET/BIG-Bench-Hard/bbh/be_1.csv'
data1 = pd.read_csv(csv_file_path1)
data2 = pd.read_csv(csv_file_path2)
selected_columns_data1 = data1[['input', 'target']]
selected_columns_data2 = data2[['input', 'predicted']]
merged_columns = pd.concat([selected_columns_data1, selected_columns_data2], axis=1)
output_file_path = 'Compare.csv'
merged_columns.to_csv(output_file_path, index=False)
print(f'Selected columns saved to {output_file_path}')

# Load the CSV file
csv_file_path = 'Compare.csv'
df = pd.read_csv(csv_file_path)

# Define a function to extract true/false from the predicted column
def extract_true_false(predicted_text):
    pattern = r'(?i)(true|false)'  # Case-insensitive pattern to match 'true' or 'false'
    match = re.search(pattern, predicted_text)
    if match:
        return match.group(1).lower()  # Return the matched value in lowercase
    else:
        return None  # Return None if no match is found

# Apply the extract_true_false function to the 'predicted' column
df['extracted_prediction'] = df['predicted'].apply(extract_true_false)

# Calculate the accuracy
accurate_rows = df[df['extracted_prediction'] == df['target']]
accuracy = len(accurate_rows) / len(df)
print(f'Accuracy: {accuracy:.3f}')