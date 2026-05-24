import os
from typing import List, Dict, Any
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

class AnalystAgent:
    """
    Agent responsible for financial reporting and strategic analysis.
    """
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def analyze_trend(self, transactions: List[Dict[str, Any]]) -> str:
        prompt = f"Analyze these transactions and provide a 1-sentence strategic insight for the accountant: {transactions}"

        message = self.client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text

analyst = AnalystAgent()
