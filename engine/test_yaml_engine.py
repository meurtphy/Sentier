import pandas as pd
from yaml_engine import load_rules, evaluate_rules

# Charger les règles YAML
rules = load_rules("tree_rules.yaml")

# Charger les features
df = pd.read_csv("features_preview.csv")

# Colonnes d'entrée = toutes sauf la colonne "match"
feature_cols = [col for col in df.columns if col != "match"]

# Stats
total = len(df)
correct = 0
errors = []

for i, row in df.iterrows():
    input_dict = {col: row[col] for col in feature_cols}
    prediction = evaluate_rules(rules, input_dict)
    expected = bool(row["match"])
    if prediction == expected:
        correct += 1
    else:
        errors.append((i, prediction, expected))

# Résultat
accuracy = correct / total * 100
print(f"\n🧪 Résultats YAML Engine : {correct}/{total} corrects → {accuracy:.2f}%")

# Afficher les erreurs
if errors:
    print("\n❌ Cas incorrects :")
    for idx, pred, exp in errors:
        print(f"- Ligne {idx} → Prévu : {pred}, Attendu : {exp}")
else:
    print("\n✅ Tous les cas sont bons !")
