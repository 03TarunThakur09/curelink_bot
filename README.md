# Curelink Patient Query Automation
This project automates responses to patient queries related to dietary intake and prescribed diet plans. The AI-driven solution is designed to replace human effort in care delivery, generating compassionate and accurate responses based on patient profiles, diet charts, and all the important factors which helps to solve the patient queries.
## Project Overview
The project uses Language Learning Models (LLMs) to generate responses that address discrepancies between a patient's reported dietary intake and their prescribed diet plan. It leverages patient profiles, chat history, and diet charts to create personalized and empathetic messages, streamlining the communication process in patient care
## Key Features
- **Patient Profile Analysis**: Integrates patient details to customize responses.
- **Chat History Integration**: Uses past conversations to maintain context and continuity in responses.
- **Diet Chart Processing**: Compares reported intake with prescribed diet plans, highlighting discrepancies.
- **Empathetic Response Generation**: Produces concise, compassionate responses tailored to the patient’s communication style.
## Project Structure

## `init_prompt.py`

### Purpose
The `init_prompt.py` file is responsible for processing meal pictures sent by patients. For each meal picture, the script determines the ideal meal the patient should be consuming at that specific day and time, according to the diet chart provided. The diet chart includes a start date, and meals are consumed in a specific order based on this date. The file includes functions to extract meal details, determine meal timings, and format the meal data for further processing.

### Key Functions

- **`process_diet_chart`**: Here we prepare the certain data structure where it have the design timing as per the diet plan.
- **`extract_ticket_info`**: Retrieves ticket creation information like ticket_id and ticket_created(To identify the patient's current time and extract the specific diet plan accordingly).
- **`convert_to_datetime`**: Converts ticket creation time to a datetime object.
- **`extract_weekday`**: Identifies the day of the week based on the ticket creation date.
- **`find_meal_time`**: Determines the meal time based on the provided timings and weekday.
- **`get_meal_notes`**: Gathers meal notes to compare with the patient's diet plan.

## `llm_prompt.py`

### Purpose
The `llm_prompt.py` file is designed to automate the response generation process using a large language model (LLM). It processes patient queries and diet plans, formats the data into a prompt, and generates responses using the LLM.
### Key Functions

- **`format_chat_history`**: Formats the chat history for use in the prompt.
- **`process_data`**: Main function that processes the patient data based on the ticket ID, extracts relevant meal details, and generates a response using the LLM.
- **`chain`**: A chain of prompts and models that generates the final response.

### Improvement

- **LLMs**: Here we use GPT models instead of we can use also open source(for costing) and other advanced LLMs to enhance response accuracy and naturalness.
- **Prompt engineering**: By providing the more context in input prompt like by in-depth context of the patient information the genrated response will be improved and also by doint prompt engineering.
- **AI Agents**: We can bulid custom AI agents for this.

## How to Use

1. **Set up OpenAI API Key**:
   - Set the OpenAI API key by replacing `"openai-apikey"` with your actual key in `llm_prompt.py`.

2. **Prepare the `queries.json` File**:
   - Ensure the `queries.json` file contains relevant patient data, diet charts, and chat context.

3. **Run the Script**:
   - Execute `llm_prompt.py` by providing a `ticket_id` when prompted. The script will generate response to the patient and save the response in `output.json`.

4. **View Results**:
   - The generated response, along with the ideal response, will be saved in `output_results_test.json`.

## Requirements

- Python 3.7+
- `langchain`
- `openai`
