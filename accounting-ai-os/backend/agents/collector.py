import os
from typing import Dict, Any
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

class CollectorAgent:
    """
    Agent responsible for ingesting data and categorizing accounting documents.
    """
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def process_document(self, text_content: str) -> Dict[str, Any]:
        prompt = f"Analyze the following accounting text and extract: Invoice Number, Date, Total Amount, Tax Amount, and Vendor. Format as a clean JSON object.\n\nText: {text_content}"

        message = self.client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        # The model returns text, we attempt to parse it as JSON
        try:
            import json
            return json.loads(message.content[0].text)
        except:
            return {"raw_text": message.content[0].text, "error": "JSON parsing failed"}

collector = CollectorAgent()
