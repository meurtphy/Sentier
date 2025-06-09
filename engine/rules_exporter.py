import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text
import yaml
import joblib

# Charger les données (mêmes features que pour train)
df = pd.read_csv("features_preview.csv")
X = df.drop(columns=["match"])
y = df["match"]

# Recréer le modèle (doit être le même que dans train_tree.py)
model = DecisionTreeClassifier(max_depth=5, random_state=42)
model.fit(X, y)

# Export texte brut
tree_text = export_text(model, feature_names=list(X.columns))
print("\n🌳 Règles apprises (format texte) :\n")
print(tree_text)

# Convertir texte en pseudo-YAML (simple indentation pour le moment)
def parse_tree(text):
    lines = text.strip().split("\n")
    yaml_rules = []
    stack = []

    for line in lines:
        depth = line.count("|   ")
        rule = line.split("|---")[-1].strip()

        node = {"depth": depth, "rule": rule}
        yaml_rules.append(node)

    return yaml_rules

rules = parse_tree(tree_text)

# Structure simple en YAML
yaml_data = []
for r in rules:
    indent = "  " * r["depth"]
    yaml_data.append(f"{indent}- {r['rule']}")

yaml_string = "\n".join(yaml_data)

# Export YAML
with open("tree_rules.yaml", "w") as f:
    f.write("# Arbre de décision converti en logique lisible\n")
    f.write(yaml_string)

print("\n✅ Export YAML terminé → tree_rules.yaml")
