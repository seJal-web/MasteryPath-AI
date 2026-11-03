import re
import pymupdf


def extract_text_from_pdf(pdf_file):
    """Extract readable text from the uploaded PDF."""
    data = pdf_file.read()

    if not data:
        return ""

    document = pymupdf.open(stream=data, filetype="pdf")
    pages = []

    try:
        for page in document:
            page_text = page.get_text("text")
            if page_text:
                pages.append(page_text)
    finally:
        document.close()

    return "\n".join(pages)


def clean_text(text):
    """Clean whitespace while keeping sentence boundaries."""
    if not text:
        return ""

    text = text.replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _sentences(text):
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []

    parts = re.split(r"(?<=[.!?])\s+", text)
    result = []
    seen = set()

    for part in parts:
        part = re.sub(r"\s+", " ", part).strip()
        if len(part) < 30:
            continue

        key = part.lower()
        if key in seen:
            continue

        seen.add(key)
        result.append(part)

    return result


def divide_into_three_parts(text):
    """Divide PDF content into three sentence-safe learning modules.

    Always returns exactly three strings, preventing the NoneType unpacking
    error and avoiding cuts in the middle of sentences whenever possible.
    """
    if not text or not text.strip():
        return "", "", ""

    sentences = _sentences(text)

    if len(sentences) < 3:
        clean = re.sub(r"\s+", " ", text).strip()
        length = len(clean)
        one_third = max(1, length // 3)
        return (
            clean[:one_third],
            clean[one_third:one_third * 2],
            clean[one_third * 2:]
        )

    total = len(sentences)
    first_end = max(1, total // 3)
    second_end = max(first_end + 1, (total * 2) // 3)

    part1 = " ".join(sentences[:first_end]).strip()
    part2 = " ".join(sentences[first_end:second_end]).strip()
    part3 = " ".join(sentences[second_end:]).strip()

    # Safety fallback: never return an empty module.
    if not part1:
        part1 = sentences[0]
    if not part2:
        part2 = sentences[min(first_end, total - 1)]
    if not part3:
        part3 = sentences[-1]

    return part1, part2, part3

