# main.py

import os
import json
from datetime import datetime
from modules.parser import extract_pdf_sections
from modules.ranker import rank_sections_by_relevance
from modules.formatter import format_output

# Configure which collections to process
COLLECTIONS = {
    "Collection 1": "Challenge_1b/Collection 1",
    "Collection 2": "Challenge_1b/Collection 2",
    "Collection 3": "Challenge_1b/Collection 3"
}

def process_collection(name, path):
    input_json = os.path.join(path, "challenge1b_input.json")
    output_json = os.path.join(path, "challenge1b_output.json")
    pdf_dir = os.path.join(path, "PDFs")

    print(f"\n🚀 Processing {name}...")

    try:
        with open(input_json, 'r', encoding='utf-8') as f:
            input_data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Skipping {name}: Input file not found.")
        return

    persona = input_data["persona"]["role"]
    task = input_data["job_to_be_done"]["task"]
    document_entries = input_data["documents"]
    document_paths = [(entry["filename"], os.path.join(pdf_dir, entry["filename"])) for entry in document_entries]

    # Extract sections from all PDFs
    extracted_sections = extract_pdf_sections(document_paths)

    # Rank by semantic relevance
    ranked_sections = rank_sections_by_relevance(extracted_sections, persona, task)

    # Create metadata and format output
    metadata = {
        "input_documents": [doc["filename"] for doc in document_entries],
        "persona": persona,
        "job_to_be_done": task,
        "timestamp": datetime.now().isoformat()
    }

    output_data = format_output(metadata, ranked_sections)

    # Write output JSON
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2)

    print(f"✅ Output written to {output_json}")


def main():
    for name, path in COLLECTIONS.items():
        process_collection(name, path)


if __name__ == "__main__":
    main()
