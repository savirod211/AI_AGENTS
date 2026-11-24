
import os
import json
from dotenv import load_dotenv
from strands import Agent, tool
from strands.models.gemini import GeminiModel

# Load GEMINI_API_KEY safely from your local .env file
# Dont forget to delete the Key on AI Studio. 
# We need to design the next agent on AWS Bedrock. My laptop cannot push it anymore. 

load_dotenv()

# Tool 1: Custom budget calculator
@tool
def calculate_trip_budget(days: int, daily_food_eur: float, hotel_per_night_eur: float) -> str:
    """Calculate the total estimated cost of a trip in Euros."""
    print("🧮 Tool 1 running: Calculating budget...")
    total = (days * daily_food_eur) + ((days - 1) * hotel_per_night_eur)
    return f"Estimated total for {days} days ({days - 1} nights): €{total:.2f}"

# Tool 2: Local file saver
# Why do we need to save this on my Laptop? WTF! 

@tool
def save_note_to_file(filename: str, content: str) -> str:
    """Save text content into a local file on the user's computer."""
    print(f"💾 Tool 2 running: Writing {filename}...")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Successfully saved file: {os.path.abspath(filename)}"

# The Gemini Model here is the brain and our agent is using it. 
model = GeminiModel(model_id="gemini-3.8-flash")

# We are creating the agent with instructions and assigning tools to it. The agent will use this as its boundary. 
agent = Agent(
    model=model,
    system_prompt=(
        "You are a helpful, practical travel planning agent. "
        "Always use your tools to calculate exact numbers and save summaries when asked."
    ),
    tools=[calculate_trip_budget, save_note_to_file],
)

# Run a multi-step goal
prompt = (
    "Plan a 3-day weekend trip to Lisbon. Assume €45/day for food and €110/night for a hotel. "
    "Use your calculator tool to get the exact budget, write a short day-by-day itinerary, "
    "and save the whole plan to a file called 'lisbon_plan.txt'."
)

print("🤖 Agent starting work...\n")
agent(prompt)

print("\n--- RAW BACK-AND-FORTH DATA ---")
print(json.dumps(agent.messages, indent=2, default=str))


# python -m venv venv
# cd .\venv\Scripts\
# venv\Scripts\activate
# pip install 'strands-agents[gemini]' python-dotenv
