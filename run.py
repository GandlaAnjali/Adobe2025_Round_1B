import json
import os
from persona_analyzer import generate_output

if __name__ == "__main__":
    input_dir = "input"
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # Load Persona JSON
    persona_file = os.path.join(input_dir, "persona.json")
    with open(persona_file, "r", encoding="utf-8") as f:
        persona_data = json.load(f)

    persona = persona_data["persona"]
    job_to_be_done = persona_data["job_to_be_done"]

    output_path = os.path.join(output_dir, "output.json")

    print("🔄 Processing PDFs based on persona & job...")
    generate_output(input_dir, persona, job_to_be_done, output_path)

    print(f" Output saved to {output_path}")
