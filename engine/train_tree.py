import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt

# 📥 Charger les données
df = pd.read_csv("features_preview.csv")

# 🧹 Séparer les features et la cible
X = df.drop(columns=["match"])
y = df["match"]

# 🔀 Découper en train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 🌳 Créer et entraîner le modèle
model = DecisionTreeClassifier(max_depth=5, random_state=42)
model.fit(X_train, y_train)

# 🧠 Afficher les règles apprises (texte)
print("\n🌳 Règles de l'arbre de décision :\n")
print(export_text(model, feature_names=list(X.columns)))

# 📈 Évaluation
y_pred = model.predict(X_test)
print("\n📊 Rapport de performance :\n")
print(classification_report(y_test, y_pred))

# 📊 Visualisation graphique (facultatif)
plt.figure(figsize=(16, 8))
plot_tree(model, feature_names=X.columns, class_names=["NO MATCH", "MATCH"], filled=True)
plt.title("Arbre de décision – Picser")
plt.savefig("tree_rules.png")
print("\n📂 Arbre visuel exporté → tree_rules.png")
print(f"📊 Taille du dataset total : {len(df)}")
print(f"🔬 Taille du jeu de test : {len(X_test)}")
plt.show()
