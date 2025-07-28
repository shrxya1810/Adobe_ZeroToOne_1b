# modules/ranker.py

from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("./models/all-MiniLM-L6-v2")

def build_query(persona, task):
    return (
        f"You are a {persona}. Your task is: {task}. "
        f"Only include content that directly helps you accomplish this task — "
        f"ignore general definitions, filler text, or introductory fluff. "
        f"Focus on action-oriented, role-relevant, and outcome-driven information "
        f"that could help someone who needs to solve this problem right now."
    )

def passes_soft_filter(section):
    # Reject short or generic text blocks
    if len(section['content']) < 100:
        return False
    if any(term in section['content'].lower() for term in [
        "introduction", "about this document", "serve hot", "n/a", "general info"
    ]):
        return False
    return True

def rank_sections_by_relevance(sections, persona, task):
    query = build_query(persona, task)
    query_embedding = model.encode(query, convert_to_tensor=True)

    scored = []
    used_docs = set()

    for section in sections:
        if not passes_soft_filter(section):
            continue

        combined = (
            f"Title: {section['section_title']}\n"
            f"Details: {section['content']}"
        )

        section_embedding = model.encode(combined, convert_to_tensor=True)
        score = util.cos_sim(query_embedding, section_embedding).item()

        # Boost diversity: penalize duplicate document picks
        doc_penalty = 0.05 if section['document'] in used_docs else 0
        used_docs.add(section['document'])

        final_score = score - doc_penalty

        scored.append((final_score, section))

    scored.sort(reverse=True, key=lambda x: x[0])

    ranked_sections = []
    for rank, (score, section) in enumerate(scored, start=1):
        section["importance_rank"] = rank
        ranked_sections.append(section)

    return ranked_sections
