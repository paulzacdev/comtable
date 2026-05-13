import os
from typing import List, Dict, Any
from pydantic import BaseModel
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

class Document(BaseModel):
    content: str
    metadata: Dict[str, Any]
    category: str = "uncategorized"

class CollectorAgent:
    """
    Agent responsible for ingesting data, performing OCR,
    and categorizing accounting documents.
    """
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def extract_data(self, text_content: str) -> Dict[str, Any]:
        prompt = f"Analyze the following accounting text and extract: Invoice Number, Date, Total Amount, Tax Amount, and Vendor. Format as JSON.\n\nText: {text_content}"

        message = self.client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text

    def categorize_document(self, extracted_data: str) -> str:
        prompt = f"Based on this extracted data: {extracted_data}, categorize this document as 'Expense', 'Income', or 'Tax'. Return only the category name."

        message = self.client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=10,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text.strip()

# Singleton instance
collector = CollectorAgent()
