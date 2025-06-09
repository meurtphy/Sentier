# test_global_matcher.py

import json
from match import match
import pandas as pd

# Charger les paires enrichies
with open("enriched_matchmaking_dataset.jsonl", "r") as f:
    lines = [json.loads(l) for l in f if l.strip()]

# Résultats
results = []

for i, entry in enumerate(lines):
    seeker = entry["seeker"]
    candidate = entry["candidate"]
    expected = entry["match"]

    predicted, reason = match(seeker, candidate)
    predicted_bool = predicted == "MATCH"

    results.append({
        "index": i,
        "expected": expected,
        "predicted": predicted_bool,
        "reason": reason,
        "ok": expected == predicted_bool
    })

df = pd.DataFrame(results)

# Résumé global
total = len(df)
correct = df["ok"].sum()
accuracy = correct / total * 100

print(f"🔎 Analyse sur {total} paires")
print(f"✅ Corrects : {correct}")
print(f"❌ Incorrects : {total - correct}")
print(f"📊 Précision brute : {accuracy:.1f}%\n")

# Cas problématiques
print("🚨 Cas divergents (faux positifs/négatifs) :\n")
divergents = df[~df["ok"]][["index", "expected", "predicted", "reason"]]
print(divergents.to_string(index=False))

# Option : export CSV si besoin
df.to_csv("test_match_results.csv", index=False)
