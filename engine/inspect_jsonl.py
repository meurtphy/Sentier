import json

with open("enriched_matchmaking_dataset.jsonl", "r", encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        print(f"\n--- 📄 Ligne {i} ---")
        try:
            obj = json.loads(line)
            print(json.dumps(obj, indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"[❌ Erreur JSON ligne {i}] {e}")
        if i >= 3:
            break
