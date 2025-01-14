from agency_swarm.agents import Agent


class PersonalAssistant(Agent):
    def __init__(self):
        super().__init__(
            name="PersonalAssistant",
            description="A personal assistant agent capable of managing emails, calendar, and time-related tasks",
            instructions="./instructions.md",
            files_folder="./files",
            schemas_folder="./schemas",
            tools=[],
            tools_folder="./tools",
            temperature=0.3,
            max_prompt_tokens=25000,
        )

    def response_validator(self, message):
        return message
