from build_features import build_dataset

# Charge les données depuis ton fichier JSONL
df = build_dataset("enriched_matchmaking_dataset.jsonl")

# Affiche un aperçu lisible
print("✅ Données chargées avec succès !")
print("🔍 Aperçu des 10 premières lignes :\n")
print(df.head(10))

# (Optionnel) Export en CSV pour inspection dans Excel
df.to_csv("features_preview.csv", index=False)
print("\n📦 Exporté vers features_preview.csv")
