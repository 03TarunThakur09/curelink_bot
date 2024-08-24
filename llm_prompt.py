import json
import os
from langchain_openai import OpenAI, ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import LLMChain
from init_prompt import *

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = "API-KEY"

# Initialize language models
llm = OpenAI()
model = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.1,
    max_tokens=100
)

# Load data from JSON file
with open('queries.json') as f:
    data = json.load(f)

def format_chat_history(data):
    """
    Format the chat history for the prompt.
    """
    chat_history = data["chat_context"]["chat_history"]
    messages = [(entry['role'], entry['message']) for entry in chat_history]
    message_strings = [f"Role: {role}, Message: {message}" for role, message in messages]
    result_string = '\n'.join(message_strings)
    return result_string, messages[-1]

# Define the prompt template
prompt_template = PromptTemplate(
    input_variables=["latest_queries", "diet_plan", "full_diet_plan", "patient_profile","last_query"],
    template=(
        "You are a compassionate medical professional responding to a patient based on their dietary intake and a prescribed diet plan. Use the following information to generate your response:\n\n"
        "1. **Patient Profile**: {patient_profile}\n"
        "1. **Patient's Previous Conversation with doctors**: {latest_queries}\n"
        "2. **Diet Plan**: {diet_plan}\n"
        "3. **Full diet plan for particular time period**: {full_diet_plan}\n"
        "Based on the conversation you have to reply for latest query that is {last_query} but also keep in mind of the previous conversation also which is very important.\n"
        "**Focus Points:**\n"
        "1. **Identify and List Foods**: Identify and list all the foods mentioned by the patient in their latest queries[Note: do note menrioned in response].\n"
        "2. **Compare with Diet Plan**: Compare these foods with those specified in the diet plan.\n"
        "3. **Address Discrepancies**: Specifically, mention any discrepancies or foods included by the patient that are not part of the diet plan. Address these discrepancies in your response(it's important).\n"
        "Otherwise, no need to give the details of food.\n"
        "**Response Requirements:**\n"
        "- Generate the ideal response to the patient in a concise form, typically in the same messaging language/style as the patient. If the patient uses informal language or mixes languages (e.g., English and Hindi), the response should reflect that.\n"
        "- Focus on addressing discrepancies in the diet with empathy and a gentle tone and do not include like user and patient name.\n"
        "- Limit the response to around 100 words or less.\n"
        "- Begin with a friendly tone, and keep the message short and focused on any deviations from the diet plan."
        "- **Language and Style**: Match the language and style of your response to the language and style used by the patient. If the patient communicates in Hinglish (a mix of Hindi and English), respond in Hinglish. If the patient uses a specific informal or mixed language style, your response should mirror that.\n"
    )
)


# Create the chain for processing the prompt
chain = prompt_template | model

def process_data(ticket_id):
    """
    Process the data based on the provided ticket_id.
    """
    data_entry = next((r for r in data if r["chat_context"]["ticket_id"] == ticket_id), None)
    if not data_entry:
        print(f"No record found for ticket ID: {ticket_id}")
        return
    
    meal_details = process_diet_chart(data_entry)
    ticket_created, ticket_id = extract_ticket_info(data_entry)
    ticket_created_datetime = convert_to_datetime(ticket_created)
    weekday_name = extract_weekday(ticket_created_datetime)
    meal_time = find_meal_time(meal_timings, ticket_created_datetime) if ticket_created_datetime else "Invalid datetime"
    diet_plan, full_diet_plan, patient_profile = get_meal_notes(data_entry, meal_details, meal_time, weekday_name)
    
    latest_queries, last_query = format_chat_history(data_entry)

    formatted_prompt = prompt_template.format(
        latest_queries=latest_queries,
        diet_plan=diet_plan,
        patient_profile=patient_profile,
        full_diet_plan=full_diet_plan,
        last_query  = last_query
    )

    print(formatted_prompt)
    response = chain.invoke({
        "latest_queries": latest_queries,
        "patient_profile": patient_profile,
        "diet_plan": diet_plan,
        "full_diet_plan": full_diet_plan,
        "last_query":last_query
    })
    
    generated_answer = response.content
    ideal_respons = ideal_response(data_entry)

    result = {
        "ticket_id": ticket_id,
        "latest_query": last_query,
        "generated_response": generated_answer,
        "ideal_response": ideal_respons
    }

    # Save results to JSON file
    with open('output_test.json', 'w') as json_file:
        json.dump(result, json_file, indent=4)
    
    print(f"Ideal response is: {ideal_respons}")

if __name__ == "__main__":
    ticket_id = input("Enter the ticket ID: ")
    process_data(ticket_id)
