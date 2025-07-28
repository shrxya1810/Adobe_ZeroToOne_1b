import os
import json
from pathlib import Path
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import fuzz
from bert_score import score as bert_score

# -----------------------------
# ✅ CONFIGURATION
# -----------------------------
BASE_DIR = "Challenge_1b"
EXPECTED_DIR = "Expected Outputs"
EXPECTED_MAP = {
    "Collection 1": "challenge1b_output_expected_coll1.json",
    "Collection 2": "challenge1b_output_expected_coll2.json",
    "Collection 3": "challenge1b_output_expected_coll3.json"
}

# -----------------------------
# ✅ MODEL SETUP
# -----------------------------
rouge = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
smooth_fn = SmoothingFunction().method4
sbert_model = SentenceTransformer("all-MiniLM-L6-v2")


# -----------------------------
# 📦 HELPERS
# -----------------------------
def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def jaccard_similarity(expected, generated):
    expected_titles = set(s["section_title"].strip().lower() for s in expected)
    generated_titles = set(s["section_title"].strip().lower() for s in generated)
    if not expected_titles or not generated_titles:
        return 0
    return len(expected_titles & generated_titles) / len(expected_titles | generated_titles)

def fuzzy_similarity(expected, generated):
    scores = []
    expected_titles = [s["section_title"].strip().lower() for s in expected]
    generated_titles = [s["section_title"].strip().lower() for s in generated]
    for et in expected_titles:
        best = max([fuzz.ratio(et, gt)/100 for gt in generated_titles], default=0)
        scores.append(best)
    return sum(scores)/len(scores) if scores else 0

def compute_rouge_bleu(expected, generated):
    rouge_scores, bleu_scores = [], []
    for e, g in zip(expected, generated):
        ref = e.get("refined_text", "").strip()
        hyp = g.get("refined_text", "").strip()
        if not ref or not hyp:
            continue
        rouge_f1 = rouge.score(ref, hyp)['rougeL'].fmeasure
        bleu = sentence_bleu([ref.split()], hyp.split(), smoothing_function=smooth_fn)
        rouge_scores.append(rouge_f1)
        bleu_scores.append(bleu)
    return (
        sum(rouge_scores) / len(rouge_scores) if rouge_scores else 0,
        sum(bleu_scores) / len(bleu_scores) if bleu_scores else 0
    )

def compute_bert(expected, generated):
    refs = [s["refined_text"] for s in expected if s["refined_text"].strip()]
    hyps = [s["refined_text"] for s in generated if s["refined_text"].strip()]
    if not refs or not hyps:
        return 0
    _, _, f1 = bert_score(hyps, refs, lang="en", verbose=False)
    return f1.mean().item()

def compute_sbert(expected, generated):
    refs = [s["refined_text"] for s in expected if s["refined_text"].strip()]
    hyps = [s["refined_text"] for s in generated if s["refined_text"].strip()]
    if not refs or not hyps:
        return 0
    ref_embeds = sbert_model.encode(refs, convert_to_tensor=True)
    hyp_embeds = sbert_model.encode(hyps, convert_to_tensor=True)
    sims = cosine_similarity(ref_embeds.cpu(), hyp_embeds.cpu())
    return sims.max(axis=1).mean()


# -----------------------------
# ✅ EVALUATION FUNCTION
# -----------------------------
def evaluate_collection(coll_name, expected_file):
    pred_path = os.path.join(BASE_DIR, coll_name, "challenge1b_output.json")
    gold_path = os.path.join(EXPECTED_DIR, expected_file)

    if not os.path.exists(pred_path) or not os.path.exists(gold_path):
        print(f"⚠️ Skipping {coll_name}: Missing files.")
        return None

    pred = load_json(pred_path)
    gold = load_json(gold_path)

    jaccard = jaccard_similarity(gold["extracted_sections"], pred["extracted_sections"])
    fuzzy = fuzzy_similarity(gold["extracted_sections"], pred["extracted_sections"])
    rougeL, bleu = compute_rouge_bleu(gold["subsection_analysis"], pred["subsection_analysis"])
    bert = compute_bert(gold["subsection_analysis"], pred["subsection_analysis"])
    sbert = compute_sbert(gold["subsection_analysis"], pred["subsection_analysis"])

    macro_f1 = (rougeL + bleu + bert + sbert) / 4

    return {
        "Collection": coll_name,
        "Section_Title_Jaccard": round(jaccard, 4),
        "Section_Title_Fuzzy": round(fuzzy, 4),
        "ROUGE-L": round(rougeL, 4),
        "BLEU": round(bleu, 4),
        "BERTScore_F1": round(bert, 4),
        "SBERT_Cosine": round(sbert, 4),
        "Macro_F1": round(macro_f1, 4)
    }


# -----------------------------
# ✅ MAIN EXECUTION
# -----------------------------
def main():
    results = []

    for coll in EXPECTED_MAP:
        expected_file = EXPECTED_MAP[coll]
        res = evaluate_collection(coll, expected_file)
        if res:
            results.append(res)
            print(f"\n📁 {coll} Evaluation")
            for k, v in res.items():
                if k != "Collection":
                    print(f"{k:>22}: {v:.4f}")

    # Average Macro F1
    avg_f1 = sum(r["Macro_F1"] for r in results) / len(results) if results else 0.0
    print(f"\n📊 Average Macro F1: {avg_f1:.4f}")

    # Save to CSV
    out_file = "final_evaluation_scores.csv"
    import csv
    with open(out_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print(f"✅ Evaluation results saved to: {out_file}")

if __name__ == "__main__":
    main()
