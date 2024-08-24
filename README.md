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

### `init.py`

This file includes functions to:

- Process diet charts and extract meal details.
- Determine meal timings based on patient queries.
- Generate responses based on patient profiles and diet history.

### `llm_prompt.py`

This file handles:

- Loading and formatting chat history.
- Defining the prompt template for response generation.
- Processing data based on the provided ticket ID.
- Generating and saving the response, along with the ideal response, in `output_results_test.json`.

### `queries.json`

This JSON file contains the data used for processing, including patient profiles, diet charts, and chat history.

## How to Use

1. **Set up OpenAI API Key**:
   - Set the OpenAI API key by replacing `"openai-apikey"` with your actual key in `llm_prompt.py`.

2. **Prepare the `queries.json` File**:
   - Ensure the `queries.json` file contains relevant patient data, diet charts, and chat context.

3. **Run the Script**:
   - Execute `llm_prompt.py` by providing a `ticket_id` when prompted. The script will generate and save the response in `output_results_test.json`.

4. **View Results**:
   - The generated response, along with the ideal response, will be saved in `output_results_test.json`.

## Requirements

- Python 3.7+
- `langchain`
- `openai`
- Other dependencies listed in `requirements.txt`

## Example Usage

```bash
