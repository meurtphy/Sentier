# Picasee

Picasee fait correspondre associations et entreprises à impact social.

## Installation

1. **Prérequis** : Python 3.12+.
2. Installez les dépendances nécessaires :
   ```bash
   pip install flask requests geopy pandas scikit-learn matplotlib pyyaml
   ```

## Lancer l'application

Lancez le microservice d'IA puis l'API principale :

```bash
python paibot2/app.py &  # microservice d'enrichissement dynamique
python engine/app.py
```

L'application expose plusieurs endpoints :
- `/` : interface HTML (dossier `frontend/`).
- `/api/match` : POST avec un profil JSON pour obtenir les entreprises compatibles.
- `/api/like` : POST pour enregistrer un like/dislike.
- `/scrape` : enrichit dynamiquement une entreprise à partir d'un nom ou d'un numéro.

## Tests

Les tests nécessitent `pytest` et d'autres dépendances (pandas, sklearn...).
Lancez-les avec :
```bash
pytest -q
```

## Contribuer

Les fichiers Python du moteur se trouvent dans `engine/`.
Le frontend statique est dans `frontend/`.
Les issues et PR sont bienvenues !
