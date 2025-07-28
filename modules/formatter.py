# modules/formatter.py

import re

def summarize_text(text, max_lines=5):
    lines = re.split(r'\n{1,2}|\.\s+', text.strip())
    meaningful = []

    for line in lines:
        line = line.strip()
        if len(line) < 50:
            continue
        if re.match(r'^[A-Z ]{5,}$', line):
            continue
        if "copyright" in line.lower() or "figure" in line.lower():
            continue
        meaningful.append(line)

    return " ".join(meaningful[:max_lines])


def format_output(metadata, ranked_sections, top_k=5):
    output = {
        "metadata": metadata,
        "extracted_sections": [],
        "subsection_analysis": []
    }

    for section in ranked_sections[:top_k]:
        output["extracted_sections"].append({
            "document": section["document"],
            "section_title": section["section_title"],
            "importance_rank": section["importance_rank"],
            "page_number": section["page"]
        })
        output["subsection_analysis"].append({
            "document": section["document"],
            "refined_text": summarize_text(section["content"]),
            "page_number": section["page"]
        })

    return output
