# Picasee

Picasee fait correspondre associations et entreprises à impact social.

## Installation

1. **Prérequis** : Python 3.12+.
2. Installez les dépendances :
   ```bash
   pip install flask requests
   ```

## Lancer l'application

```bash
python engine/app.py
```

L'application expose plusieurs endpoints :
- `/` : interface HTML (dossier `frontend/`).
- `/api/match` : POST avec un profil JSON pour obtenir les entreprises compatibles.
- `/api/like` : POST pour enregistrer un like/dislike.

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
