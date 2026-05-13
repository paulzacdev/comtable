import os
from typing import List, Dict, Any
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

class AnalystAgent:
    """
    Agent responsible for high-level financial analysis,
    cash-flow forecasting, and strategic reporting.
    """
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def generate_financial_report(self, data_summary: str) -> str:
        prompt = f"Act as a senior chartered accountant. Analyze this financial data and provide a professional summary, including key trends and 3 strategic recommendations for the client: {data_summary}"

        message = self.client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text

    def forecast_cashflow(self, history: List[Dict[str, Any]]) -> Dict[str, Any]:
        prompt = f"Based on this transaction history: {history}, predict the cash flow for the next 3 months. Provide the output in a structured JSON format with 'expected_balance' and 'risk_factors'."

        message = self.client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        return {"forecast": message.content[0].text}

# Singleton instance
analyst = AnalystAgent()
