from agency_swarm.tools import BaseTool
from datetime import datetime

class GetCurrentTime(BaseTool):
    """
    A tool for getting the current time.
    """

    def run(self):
        """
        Returns the current time in a human-readable format.
        """
        current_time = datetime.now()
        return f"Current time is: {current_time.strftime('%I:%M %p')}"

if __name__ == "__main__":
    tool = GetCurrentTime()
    print(tool.run()) 