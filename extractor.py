import fitz  # PyMuPDF
import os
import json
import re
from collections import Counter
import unicodedata

# 1. Font Size Analysis
def analyze_font_sizes(doc):
    """Analyze font sizes across the document to identify unique font sizes."""
    sizes = []
    for page in doc:
        for b in page.get_text("dict")["blocks"]:
            if "lines" in b:
                for line in b["lines"]:
                    for span in line["spans"]:
                        sizes.append(round(span["size"], 1))
    return sorted(set(sizes), reverse=True)

# 2. Dynamic Font → Heading Level Mapping
def map_font_to_heading_levels(unique_sizes):
    """Map largest fonts to H1, H2, H3 dynamically."""
    level_map = {}
    for i, size in enumerate(unique_sizes):
        if i == 0:
            level_map[size] = "H1"
        elif i == 1:
            level_map[size] = "H2"
        elif i == 2:
            level_map[size] = "H3"
        else:
            level_map[size] = f"H{i+1}"
    return level_map

# 3. Clean Text + Multilingual Normalization
def clean_text(text):
    """Normalize multilingual text and clean extra spaces."""
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# 4. Merge Broken Headings
def merge_broken_headings(outline):
    """Merge consecutive headings with the same level on the same page."""
    merged = []
    for item in outline:
        if (
            merged
            and merged[-1]["level"] == item["level"]
            and merged[-1]["page"] == item["page"]
        ):
            merged[-1]["text"] += " " + item["text"]
            merged[-1]["text"] = clean_text(merged[-1]["text"])
        else:
            merged.append(item)
    return merged

# 5. Main Outline Extraction
def extract_outline(pdf_path):
    doc = fitz.open(pdf_path)
    unique_sizes = analyze_font_sizes(doc)
    level_map = map_font_to_heading_levels(unique_sizes)

    outline = []
    title_candidates = Counter()
    max_font_seen = 0
    title = None

    for page_num, page in enumerate(doc, start=0):  # 0-based page indexing
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if "lines" in b:
                for line in b["lines"]:
                    for span in line["spans"]:
                        text = clean_text(span["text"])
                        size = round(span["size"], 1)

                        if not text or len(text) < 2:
                            continue

                        # Skip URLs & plain page numbers
                        if re.match(r"^https?://", text) or text.isdigit():
                            continue

                        # Title candidate detection (only first 2 pages)
                        if page_num <= 1:
                            title_candidates[text] += 1
                            if size > max_font_seen:
                                max_font_seen = size
                                title = text

                        # Heading detection
                        if size in level_map:
                            outline.append(
                                {
                                    "level": level_map[size],
                                    "text": text,
                                    "page": page_num,
                                }
                            )

    # Merge Broken Headings
    outline = merge_broken_headings(outline)

    # Finalize Title — Prefer first H1 after merging
    first_h1 = next((item["text"] for item in outline if item["level"] == "H1"), None)
    if first_h1:
        title = first_h1
    elif not title and title_candidates:
        title = title_candidates.most_common(1)[0][0]

    title = clean_text(title or "Untitled Document")

    return {
        "title": title,
        "outline": outline,
    }

# 6. Process All PDFs
def process_all_pdfs(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_dir, filename)
            result = extract_outline(pdf_path)
            output_file = os.path.join(output_dir, filename.replace(".pdf", ".json"))
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

# 7. Main Execution
if __name__ == "__main__":
    input_dir = "input"
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    process_all_pdfs(input_dir, output_dir)
