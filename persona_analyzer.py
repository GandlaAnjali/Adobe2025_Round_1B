import fitz  # PyMuPDF
import os
import re
import json
import unicodedata
from datetime import datetime

# Small Synonyms Dictionary (expandable)
SYNONYMS = {
    "methodology": ["approach", "technique", "procedure"],
    "dataset": ["data", "corpus", "records"],
    "performance": ["accuracy", "efficiency", "results"],
    "analysis": ["evaluation", "examination", "assessment"],
    "review": ["survey", "summary", "overview"]
}

# Clean & Normalize text (Multilingual Safe)
def clean_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip().lower()

# Split into paragraphs
def split_into_paragraphs(text: str):
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]

# Expand keywords with synonyms
def expand_keywords(keywords):
    expanded = set(keywords)
    for kw in keywords:
        for syn, syn_list in SYNONYMS.items():
            if kw == syn or kw in syn_list:
                expanded.add(syn)
                expanded.update(syn_list)
    return expanded

# Scoring Function
def calculate_relevance_score(text, persona_terms, job_terms):
    score = 0
    for term in persona_terms:
        score += text.count(term) * 1
    for term in job_terms:
        score += text.count(term) * 3
    return score

# Extract relevant sections (sorted & ranked)
def analyze_documents(input_dir, persona_terms, job_terms):
    results = []
    for filename in os.listdir(input_dir):
        if not filename.endswith(".pdf"):
            continue

        pdf_path = os.path.join(input_dir, filename)
        doc = fitz.open(pdf_path)

        for page_num, page in enumerate(doc, start=0):  # 0-based indexing
            text = clean_text(page.get_text("text"))
            paragraphs = split_into_paragraphs(text)

            for para in paragraphs:
                score = calculate_relevance_score(para, persona_terms, job_terms)
                if score > 0:
                    results.append({
                        "document": filename,
                        "page": page_num,
                        "section_title": para[:80] + "..." if len(para) > 80 else para,
                        "importance_score": score
                    })

    # Sort by score & assign rank
    results = sorted(results, key=lambda x: x["importance_score"], reverse=True)
    for rank, r in enumerate(results, start=1):
        r["importance_rank"] = rank
        del r["importance_score"]

    # Return Only Top 20 Sections for Conciseness
    return results[:20]

# Generate Output JSON
def generate_output(input_dir, persona_data, job_to_be_done, output_path):
    # 🔹 Extract persona keywords from structured JSON
    persona_keywords = set()
    persona_keywords.update(clean_text(persona_data.get("role", "")).split())
    persona_keywords.update(clean_text(persona_data.get("expertise", "")).split())
    for fa in persona_data.get("focus_areas", []):
        persona_keywords.update(clean_text(fa).split())

    job_terms = expand_keywords(clean_text(job_to_be_done).split())
    persona_terms = expand_keywords(persona_keywords)

    extracted_sections = analyze_documents(input_dir, persona_terms, job_terms)

    output = {
        "metadata": {
            "documents": [f for f in os.listdir(input_dir) if f.endswith(".pdf")],
            "persona": persona_data,
            "job_to_be_done": job_to_be_done,
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        },
        "extracted_sections": extracted_sections
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Output saved to {output_path}")
