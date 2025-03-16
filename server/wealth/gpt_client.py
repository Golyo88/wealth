import time
import openai
from typing import Any

from wealth.model import Wealth


class ChatGPTClient:
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)

    def process_pdf_content(
        self, schema: dict[str, Any], pdf_content: str
    ) -> dict[str, Any]:
        try:
            response = self.client.beta.chat.completions.parse(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that converts PDF content to JSON. Only provide values that are present in the PDF content.",
                    },
                    {
                        "role": "user",
                        "content": f"Please convert this PDF content to JSON according to the provided schema:\n\n{pdf_content}",
                    },
                ],
                temperature=0.0,
                response_format=Wealth,
            )

            return Wealth.model_validate_json(response.choices[0].message.content)
        except openai.RateLimitError as e:
            print(f"Rate limit error: {str(e)}")
            time.sleep(10)
            return self.process_pdf_content(schema, pdf_content)
        except Exception as e:
            print(f"Error processing PDF content: {str(e)}")
            return None
