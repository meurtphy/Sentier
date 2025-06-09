import json
import pandas as pd

def safe_lower(val):
    return val.lower() if isinstance(val, str) else ""

def zone_is_compatible(seeker_zone, candidate_zone):
    seeker_zone = safe_lower(seeker_zone)
    candidate_zone = safe_lower(candidate_zone)

    if not seeker_zone or not candidate_zone:
        return False  # données incomplètes

    if seeker_zone == candidate_zone:
        return True
    if candidate_zone == "national":
        return True
    if seeker_zone == "national":
        return True  # toléré
    return False

def compute_budget_ratio(seeker_budget, candidate_budget):
    if seeker_budget <= 0:
        return 0.0
    return round(min(candidate_budget / seeker_budget, 2.0), 2)

def compute_need_overlap(seeker_needs, candidate_offers):
    if not seeker_needs:
        return 0, 0.0  # aucun besoin exprimé
    common = set(seeker_needs) & set(candidate_offers)
    count = len(common)
    ratio = round(count / len(seeker_needs), 2)
    return count, ratio

def extract_features(pair):
    seeker = pair.get("seeker", {})
    candidate = pair.get("candidate", {})

    # Champs extraits
    seeker_zone = seeker.get("zone", "")
    candidate_zone = candidate.get("zone", "")
    seeker_needs = seeker.get("constraints", [])
    candidate_offers = candidate.get("engagement", [])
    seeker_budget = seeker.get("budget_needed", 0)
    candidate_budget = candidate.get("budget_available", 0)

    zone_match = zone_is_compatible(seeker_zone, candidate_zone)
    budget_ratio = compute_budget_ratio(seeker_budget, candidate_budget)
    has_finance_need = "financier" in seeker_needs
    has_finance_offer = "financier" in candidate_offers
    financing_possible = has_finance_need and has_finance_offer and candidate_budget > 0
    overlap_count, overlap_ratio = compute_need_overlap(seeker_needs, candidate_offers)

    return {
        "zone_match": zone_match,
        "budget_ratio": budget_ratio,
        "has_finance_need": has_finance_need,
        "has_finance_offer": has_finance_offer,
        "financing_possible": financing_possible,
        "need_overlap_count": overlap_count,
        "need_overlap_ratio": overlap_ratio,
        "match": pair.get("match", False)
    }

def build_dataset(jsonl_path):
    rows = []
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            try:
                pair = json.loads(line)
                features = extract_features(pair)
                rows.append(features)
            except Exception as e:
                print(f"[❌ Ligne {i}] Erreur : {e}")
    print(f"✅ {len(rows)} lignes valides extraites.")
    return pd.DataFrame(rows)
