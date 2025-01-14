from agency_swarm import Agency
from agency_swarm.util import set_openai_key
from PersonalAssistant import PersonalAssistant
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set OpenAI API key
set_openai_key(os.getenv('OPENAI_API_KEY'))

# Initialize the personal assistant agent
assistant = PersonalAssistant()

# Create the agency with the personal assistant
agency = Agency(
    [assistant],  # Single agent agency with the personal assistant as the entry point
    shared_instructions='agency_manifesto.md',
    temperature=0.7,
    max_prompt_tokens=4000
)

if __name__ == "__main__":
    agency.run_demo()  # Start the interactive demo in terminal 