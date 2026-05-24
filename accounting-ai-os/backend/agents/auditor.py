import os
from typing import List, Dict, Any
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

class AuditorAgent:
    """
    Agent responsible for detecting anomalies and verifying tax compliance.
    """
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def audit_transaction(self, data: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"Audit this transaction for anomalies or tax errors: {data}. Return a JSON object with 'is_valid' (boolean) and 'reason' (string)."

        message = self.client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )
        try:
            import json
            return json.loads(message.content[0].text)
        except:
            return {"is_valid": False, "reason": "Audit failed to parse."}

auditor = AuditorAgent()
