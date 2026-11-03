from src.pdf_processor import extract_text_from_pdf


pdf_path = "data/pdfs/test.pdf"

with open(pdf_path, "rb") as file:
    text = extract_text_from_pdf(file)

print(text[:2000])
