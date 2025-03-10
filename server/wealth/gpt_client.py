import openai
import json
from typing import Any

from model import Wealth


class ChatGPTClient:
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)

    def process_pdf_content(
        self, schema: dict[str, Any], pdf_content: str
    ) -> dict[str, Any]:
        try:
            response = self.client.beta.chat.completions.parse(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that converts PDF content to JSON.",
                    },
                    {
                        "role": "user",
                        "content": f"Please convert this PDF content to JSON according to the provided schema:\n\n{pdf_content}",
                    },
                ],
                temperature=0.1,
                response_format=Wealth,
            )

            return Wealth.model_validate_json(response.choices[0].message.content)
        except Exception as e:
            print(f"Error processing PDF content: {str(e)}")
            return None
