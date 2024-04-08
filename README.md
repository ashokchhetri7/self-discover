### SELF-DISCOVER: Large Language Models Self-Compose Reasoning Structures

##
This is the extension from the git repo. [https://github.com/kailashsp/SelfDiscover.git]
All credit goes to this repo and the Original Paper given below:
SELF-DISCOVER: Large Language Models Self-Compose Reasoning Structures
[link](https://arxiv.org/pdf/2402.03620.pdf)

## Prerequisites

- Python 3.10
- Libraries: google-generativeai, openai, dotenv
- Input the task you want to generate a reasoning structure in task_example.py

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/ashokchhetri7/self-discover.git
   ```

2. Install the required libraries:

   ```bash
   pip install -r requirements.txt
   ```
3. create a .env file

4. Open the `.env` file in a text editor.

5. Add the following line to the `.env` file:

   ```
   GOOGLE_API_KEY= add_your_api_key_here_no_quotation_needed
   ```

   Replace `your_google_api_key_here` with your actual Google API key obtained from [google makersuite](https://makersuite.google.com/app/apikey).
   Your can also use OPENAI_API_KEY as well

## Customization

- Modify the `reasoning_modules` variable in `prompts.py` to add, remove, or modify reasoning modules.
- Adjust the prompts in `prompts.py` to customize the user interaction flow.

## How to use the reasoning JSON structure

- As mentioned in the paper 
```markdown
For Stage 2, where we use the self-discovered structure to solve the task instances, we start with the prompt: “Follow the
step-by-step reasoning plan in JSON to correctly solve the task. Fill in the values following the keys by reasoning specifically 
about the task given. Do not simply rephrase the keys.”, followed by the reasoning structure, and finally the task instance.
```

## Final Output 
- Based on the above reasoning structure and step I have given the following structure to get the final output. No need to run this. (It's not runnable) 

```markdown

Follow the step-by-step reasoning plan in {reasoning_structure} to correctly solve the task. 
Fill in the values following the keys by reasoning specifically about the task given. 
Do not simply rephrase the keys. And finally provide the "final_answer" of the given question.

For the given task; 
<Task>
{Task}
</Task>

Given reasoning steps;
{reasoning_structure}

Expected Output:
{
  "final_answer": {
    ...
    }
}

```

## Usage

1. Simply run the command below:
    
   ```bash
   python self_discover.py

   ```

## You can see that in the Streamlit also

   ```
   python streamlit run app.py
   ```
You can see the ouptut of the select, adapt, implement as well as final ouptut in the web using this command.

---

