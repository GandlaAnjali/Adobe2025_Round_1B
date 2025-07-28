# Adobe Hackathon 2025: Connecting the Dots Challenge (Round 1B)

 ## Synopsis of the Project
1. The Adobe Hackathon 2025 – Round 1B: "Persona-Driven Document Intelligence" is where this solution was created.
2. The objective is to create an intelligent document analyzer that:
3. Ranks sections according to a given persona and their job-to-be-done
4. Extracts and prioritizes relevant sections from a collection of PDFs
5. Generates an output JSON that highlights important sections with ranks
6. This serves as the basis for creating futuristic reading experiences powered by document intelligence driven by AI.

## Important Aspects
1. Persona-Driven Analysis – Understands persona role, expertise, and focus areas.
2. Job-Aware Ranking – Prioritizes sections relevant to the job-to-be-done using weighted scoring.
3. Synonyms Expansion (Bonus) – Improves semantic matching using a small synonyms dictionary.
4. Paragraph-Level Relevance – Paragraphs are examined separately for fine-grained ranking.
5. Hackathon Compliance –
  Runs fully offline (no API calls)
  Execution time ≤ 60 seconds for 3–5 PDFs
  Model size ≤ 1GB

## Folder Structure

adobe_round1b/
├── Dockerfile # Dockerized execution (mandatory for judging)

├── requirements.txt # Python dependencies

├── run.py # Entry-point script for execution

├── persona_analyzer.py # Core logic for persona-based document analysis

├── input/
│ ├── sample1.pdf # Sample PDF (test document)
│ ├── sample2.pdf # Another test PDF
│ └── persona.json # Persona & job-to-be-done definition

└── output/
└── output.json # Auto-generated ranked output

## Tech Stack
1. Language: Python 3.9
2. Libraries:
    -PyMuPDF (fitz) – PDF text extraction
    -unicodedata, re – Text cleaning & normalization
    -json, os, datetime – Output & file handling

## Execution Instructions

## 1Build the Docker Image
docker build --no-cache -t adobe_round1b .

## Run the Container
docker run --rm -v ${PWD}/input:/app/input -v ${PWD}/output:/app/output --network none adobe_round1b

## Automatic Workflow
1. All PDFs are read from /input
2. Extracts persona & job details using persona.json
3. Ranks relevant sections using weighted scoring
4. Saves ranked results to /output/output.json

## Sample Persona (persona.json)
```json
{
  "persona": {
    "role": "PhD Researcher in Computational Biology",
    "expertise": "Graph Neural Networks, Drug Discovery",
    "focus_areas": ["methodologies", "datasets", "performance benchmarks"]
  },
  "job_to_be_done": "Prepare a comprehensive literature review focusing on methodologies, datasets, and performance benchmarks."
}
```

## Sample Output (JSON)
```json

{
  "metadata": {
    "documents": ["sample1.pdf", "sample2.pdf"],
    "persona": {
      "role": "PhD Researcher in Computational Biology",
      "expertise": "Graph Neural Networks, Drug Discovery",
      "focus_areas": ["methodologies", "datasets", "performance benchmarks"]
    },
    "job_to_be_done": "Prepare a comprehensive literature review focusing on methodologies, datasets, and performance benchmarks.",
    "timestamp": "2025-07-23T14:07:43"
  },
  "extracted_sections": [
    {
      "document": "sample1.pdf",
      "page": 4,
      "section_title": "Algorithmic decision making methods for fair credit scoring – Regulatory compli...",
      "importance_rank": 1
    },
    {
      "document": "sample2.pdf",
      "page": 2,
      "section_title": "Graph neural network methodologies applied to drug discovery datasets...",
      "importance_rank": 2
    }
  ]
}
```

## Highlights 
1. Persona Understanding – Matches synonyms and keywords with persona context.
2. Ranking Accuracy – Weighted scoring ensures highest-priority sections rank at the top.
3. Performance – Handles multiple PDFs in under 60 seconds (optimized for large documents).

## Authors
1. Varsha Dubbaka
2. Gandla Anjali

## For Judges
1. Place any PDFs inside /input
2. Update persona.json with the required persona & job
3. Run the Docker commands above
4. Check /output/output.json for the ranked results

