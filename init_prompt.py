import json
from datetime import datetime

with open('queries.json') as f:
    data = json.load(f)


def parse_time(timing_str):
    """Parse a time string into a time object."""
    try:
        return datetime.strptime(timing_str, '%I:%M %p').time()
    except ValueError as e:
        print(f"Error parsing time '{timing_str}': {e}")
        return None

def extract_meal_options(meal):
    """Extract notes from meal options."""
    notes = []
    if 'meal_options' in meal:
        meal_options = meal['meal_options']
        for option in meal_options:
            if isinstance(option, dict):
                note = option.get('notes')
                if note:
                    notes.append(note)

    return notes

def extract_meal_details(meals_by_days):
    """Extract all timings, meal names, and notes, and organize them into a dictionary."""
    meal_details = {}

    for meal_day in meals_by_days:
        if isinstance(meal_day, dict) and 'meals' in meal_day:
            meals = meal_day['meals']
            for meal in meals:
                if isinstance(meal, dict):
                    meal_name = meal.get('name')
                    if meal_name:
                        timing_str = meal.get('timings')
                        notes = extract_meal_options(meal)

                        if meal_name not in meal_details:
                            meal_details[meal_name] = {"timings": [], "notes": []}

                        if timing_str:
                            time_obj = parse_time(timing_str)
                            if time_obj:
                                meal_details[meal_name]["timings"].append(time_obj)
                        meal_details[meal_name]["notes"].extend(notes)

                        # Ensure timings have exactly 7 elements
                        if len(meal_details[meal_name]["timings"]) > 7:
                            meal_details[meal_name]["timings"] = meal_details[meal_name]["timings"][:7]
                        elif len(meal_details[meal_name]["timings"]) < 7:
                            last_timing = meal_details[meal_name]["timings"][-1] if meal_details[meal_name]["timings"] else ''
                            meal_details[meal_name]["timings"].extend([last_timing] * (7 - len(meal_details[meal_name]["timings"])))

                        # Ensure notes have exactly 7 elements
                        if len(meal_details[meal_name]["notes"]) > 7:
                            meal_details[meal_name]["notes"] = meal_details[meal_name]["notes"][:7]
                        elif len(meal_details[meal_name]["notes"]) < 7:
                            last_note = meal_details[meal_name]["notes"][-1] if meal_details[meal_name]["notes"] else ''
                            meal_details[meal_name]["notes"].extend([last_note] * (7 - len(meal_details[meal_name]["notes"])))

    return meal_details


def format_meal_timings(meal_details):
    """Convert time objects to string format in the meal details dictionary."""
    for meal_name, details in meal_details.items():
        details['timings'] = [time.strftime('%H:%M:%S') for time in details['timings']]
    return meal_details

def process_diet_chart(record):
    """Process the diet chart from a single record and extract meal details."""
    if 'profile_context' in record and 'diet_chart' in record['profile_context']:
        diet_chart = record['profile_context']['diet_chart']
        if 'meals_by_days' in diet_chart:
            meals_by_days = diet_chart['meals_by_days']
            meal_details = extract_meal_details(meals_by_days)
            formatted_details = format_meal_timings(meal_details)
            return formatted_details
        else:
            print("Field 'meals_by_days' not found in 'diet_chart'.")
    else:
        print("Field 'diet_chart' or 'profile_context' not found.")
    return {}

meal_timings = {
    "Early Morning": {
        "start_time": datetime.strptime("06:30:00", "%H:%M:%S").time(),
        "end_time": datetime.strptime("08:30:00", "%H:%M:%S").time()
    },
    "Breakfast": {
        "start_time": datetime.strptime("08:30:00", "%H:%M:%S").time(),
        "end_time": datetime.strptime("11:00:00", "%H:%M:%S").time()
    },
    "Mid Meal": {
        "start_time": datetime.strptime("11:00:00", "%H:%M:%S").time(),
        "end_time": datetime.strptime("13:30:00", "%H:%M:%S").time()
    },
    "Lunch": {
        "start_time": datetime.strptime("13:30:00", "%H:%M:%S").time(),
        "end_time": datetime.strptime("17:00:00", "%H:%M:%S").time()
    },
    "Evening": {
        "start_time": datetime.strptime("17:00:00", "%H:%M:%S").time(),
        "end_time": datetime.strptime("20:00:00", "%H:%M:%S").time()
    },
    "Dinner": {
        "start_time": datetime.strptime("20:00:00", "%H:%M:%S").time(),
        "end_time": datetime.strptime("21:30:00", "%H:%M:%S").time()
    },
    "Post Dinner": {
        "start_time": datetime.strptime("21:30:00", "%H:%M:%S").time(),
        "end_time": datetime.strptime("23:59:59", "%H:%M:%S").time()
    }
}

def extract_ticket_info(data):
    if not data or 'chat_context' not in data:
        return None, None
    chat_context = data['chat_context']
    return chat_context.get('ticket_created'), chat_context.get('ticket_id')
def ideal_response(data):
    if not data or 'ideal_response' not in data:
        return None, None
    chat_context = data['ideal_response']
    return chat_context
def convert_to_datetime(date_string):
    try:
        return datetime.strptime(date_string, "%B %d, %Y, %I:%M %p")
    except ValueError:
        return None

def find_meal_time(meal_timings, timestamp):
    time_only = timestamp.time()  # Extract the time part from the timestamp
    for meal, timings in meal_timings.items():
        if timings["start_time"] <= time_only <= timings["end_time"]:
            return meal
    return "No matching meal time"

def extract_weekday(date):
    return date.strftime("%A") if date else "Invalid datetime"
def extract_content(data):
    all_content = [entry['content'] for entry in data['latest_query']]

    content_list = []
    for content in all_content:
        content_list.append(content)
    
    return content_list


def get_meal_notes(data, meal_details, meal_time, weekday_name):
    # Dictionary to map weekday names to indices
    weekday_indices = {
        'Friday': 0,
        'Saturday': 1,
        'Sunday': 2,
        'Monday': 3,
        'Tuesday': 4,
        'Wednesday': 5,
        'Thursday': 6
    }
    
    if meal_time not in meal_details:
        raise ValueError(f"Invalid meal_time: {meal_time}. Expected one of {list(meal_details.keys())}.")
    
    if weekday_name not in weekday_indices:
        raise ValueError(f"Invalid weekday_name: {weekday_name}. Expected one of {list(weekday_indices.keys())}.")
    
    weekday_index = weekday_indices[weekday_name]
    
    meal_info = meal_details[meal_time]
    timings = meal_info['timings']
    notes = meal_info['notes']
    full_notes  = data["profile_context"]["diet_chart"]["notes"]
    patient_profile = data["profile_context"]["patient_profile"]

    if len(timings) != 7 or len(notes) != 7:
        raise ValueError("Timings and notes lists must contain exactly 7 values.")
    return notes[weekday_index],full_notes, patient_profile

