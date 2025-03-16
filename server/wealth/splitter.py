import re
import os
from pypdf import PdfReader, PdfWriter


def extract_representative_name(page_text):
    match = re.search(r"A nyilatkozatot adó neve:\s*(.+)", page_text)
    if match:
        name_line = match.group(1).strip().splitlines()[0]
        safe_name = re.sub(r'[\\/*?:"<>|]', "", name_line)
        return safe_name
    return None


def split_pdf_by_representative(pdf_path, output_dir):
    reader = PdfReader(pdf_path)
    num_pages = len(reader.pages)

    representative_sections = []
    current_section = None

    for i in range(num_pages):
        page = reader.pages[i]
        text = page.extract_text() or ""
        if "A nyilatkozatot adó neve:" in text:
            if current_section is not None:
                current_section["end"] = i - 1
                representative_sections.append(current_section)
            rep_name = extract_representative_name(text)
            if not rep_name:
                rep_name = f"rep_{i}"
            current_section = {"name": rep_name, "start": i, "end": None}
    if current_section is not None:
        current_section["end"] = num_pages - 1
        representative_sections.append(current_section)

    print(f"Talált képviselői szakaszok száma: {len(representative_sections)}")

    os.makedirs(output_dir, exist_ok=True)

    for section in representative_sections:
        writer = PdfWriter()
        for i in range(section["start"], section["end"] + 1):
            writer.add_page(reader.pages[i])
        output_filename = os.path.join(
            output_dir, f"{section['name']}-{section['start']}-{section['end']}.pdf"
        )
        with open(output_filename, "wb") as out_f:
            writer.write(out_f)
        print(f"Kész: {output_filename}")


def main():
    pdf_path = "Kepviselok_dec_20230712.pdf"
    output_dir = "split_representatives"
    split_pdf_by_representative(pdf_path, output_dir)


if __name__ == "__main__":
    main()
