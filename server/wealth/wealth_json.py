import asyncio
import os
from dotenv import load_dotenv
from pathlib import Path
import json
from gpt_client import ChatGPTClient
from pdf_processor import PDFProcessor


async def main():
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY környezeti változó nincs beállítva!")

    output_dir = "output"
    gpt_client = ChatGPTClient(api_key)
    processor = PDFProcessor(
        gpt_client=gpt_client, schema_path="wealth/wealth.schema.json"
    )

    async for result in processor.process_pdfs(
        pdf_directory="split_representatives", output_dir=output_dir, max_concurrent=3
    ):
        if result["success"]:
            pdf_name = Path(result["pdf_path"]).stem
            output_path = Path(output_dir) / f"{pdf_name}.json"

            with open(output_path, "w", encoding="utf-8") as f:
                content = result["result"].model_dump_json()
                f.write(content)


if __name__ == "__main__":
    asyncio.run(main())
