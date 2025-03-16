from pydantic import BaseModel
from pypdf import PdfReader
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import AsyncGenerator, TypedDict
from gpt_client import ChatGPTClient


class Result(TypedDict):
    pdf_path: str
    result: BaseModel
    success: bool


class PDFProcessor:
    def __init__(self, gpt_client: ChatGPTClient, schema_path: str):
        self.gpt_client = gpt_client
        with open(schema_path, "r", encoding="utf-8") as f:
            self.schema = json.load(f)

    def get_processed_files(self, output_dir: Path) -> set:
        """Visszaadja a már feldolgozott PDF-ek neveit"""
        return {json_file.stem for json_file in output_dir.glob("*.json")}

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

    async def process_single_pdf(self, pdf_path: Path) -> Result:
        try:
            with ThreadPoolExecutor() as executor:
                pdf_content = await asyncio.get_event_loop().run_in_executor(
                    executor, self.extract_text_from_pdf, str(pdf_path)
                )

                result = await asyncio.get_event_loop().run_in_executor(
                    executor,
                    self.gpt_client.process_pdf_content,
                    self.schema,
                    pdf_content,
                )

            return {
                "pdf_path": str(pdf_path),
                "result": result,
                "success": bool(result),
            }
        except Exception as e:
            print(f"✗ Hiba a feldolgozás során ({pdf_path.name}): {str(e)}")
            return {
                "pdf_path": str(pdf_path),
                "result": None,
                "success": False,
                "error": str(e),
            }

    async def process_pdfs(
        self, pdf_dir: Path, output_dir: Path, max_concurrent: int = 3
    ) -> AsyncGenerator[Result, None]:
        processed_files = self.get_processed_files(output_dir)
        pdf_files = [
            pdf for pdf in pdf_dir.glob("*.pdf") if pdf.stem not in processed_files
        ]

        if not pdf_files:
            print("Minden PDF már fel van dolgozva!")
            return

        print(f"Feldolgozásra vár: {len(pdf_files)} PDF")
        print(f"Már feldolgozva: {len(processed_files)} PDF")

        for batch_start in range(0, len(pdf_files), max_concurrent):
            batch = pdf_files[batch_start : batch_start + max_concurrent]
            tasks = [self.process_single_pdf(pdf_file) for pdf_file in batch]
            results = await asyncio.gather(*tasks)

            for result in results:
                if result["success"]:
                    print(f"✓ Sikeres feldolgozás: {Path(result['pdf_path']).name}")
                yield result
