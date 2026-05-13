import os
from typing import List, Dict, Any
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

class AuditorAgent:
    """
    Agent responsible for detecting anomalies,
    verifying tax compliance, and bank reconciliation.
    """
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def check_anomalies(self, transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        prompt = f"Review these transactions for anomalies (duplicates, unusual amounts, missing tax): {transactions}. Return a list of suspicious transactions with reasons in JSON."

        message = self.client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text

    def reconcile_bank(self, bank_statement: str, ledger_entries: List[Dict[str, Any]]) -> Dict[str, Any]:
        prompt = f"Compare the bank statement: {bank_statement} with these ledger entries: {ledger_entries}. Identify any missing entries or mismatches."

        message = self.client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        return {"analysis": message.content[0].text}

# Singleton instance
auditor = AuditorAgent()
