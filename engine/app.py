# app.py
import requests  # en haut du fichier
from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime
from match import match  # Assure-toi que cette fonction existe et utilise tous les blocs
import os

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")

app = Flask(__name__)

@app.get("/")
def serve_index():
    """Point d'entrée HTML"""
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.get("/<path:filename>")
def serve_static(filename):
    """Sert les fichiers frontend"""
    return send_from_directory(FRONTEND_DIR, filename)


SCRAPER_BASE = "http://localhost:8000"   # ton micro-service scrap/PDF

@app.post("/api/enrich-company")
def enrich_company():
    """
    Proxy : reçoit { query:"…"}  (nom, SIREN/SIRET ou URL)
    → renvoie le JSON scraping du micro-service
    """
    payload = request.get_json(force=True)
    query   = payload.get("query", "").strip()
    if not query:
        return jsonify({"error": "query requis"}), 400

    try:
        r = requests.post(f"{SCRAPER_BASE}/scrape", json={"url": query}, timeout=10)
        r.raise_for_status()
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": "Scraper KO", "detail": str(e)}), 502



# 🔧 Simule une "base de données" entreprise
CANDIDATE_DB = [
    {
        "type": "entreprise",
        "name": "GreenTech",
        "engagement": ["financier", "mobilité", "logistique"],
        "budget_available": 1500,
        "location": "Paris",
        "when": "flexible"
    },
    {
        "type": "entreprise",
        "name": "StartCare",
        "engagement": ["hébergement", "financier", "aide alimentaire"],
        "budget_available": 800,
        "location": "Lyon",
        "when": "2024-09-15"
    },
    {
        "type": "entreprise",
        "name": "EduSolidar",
        "engagement": ["communication", "matériel scolaire", "financier"],
        "budget_available": 2000,
        "location": "Toulouse",
        "when": "urgent"
    }
]

# 🔄 Historique des interactions
match_log = []

@app.route("/api/like", methods=["POST"])
def like():
    """Endpoint pour enregistrer une interaction utilisateur (like/dislike)"""
    try:
        data = request.get_json()
        entry = {
            "timestamp": datetime.now().isoformat(),
            "profile": data.get("company"),
            "liked": data.get("liked")
        }
        match_log.append(entry)
        print("✅ Nouvelle interaction :", entry)
        return jsonify({"status": "ok", "message": "Interaction enregistrée"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/api/matchlog", methods=["GET"])
def get_log():
    """Retourne l’historique des likes/dislikes"""
    return jsonify(match_log), 200

@app.route("/api/match", methods=["POST"])
def get_matches():
    """Endpoint principal : reçoit un profil association et retourne les entreprises matchées"""
    try:
        seeker = request.get_json()
        if not seeker:
            return jsonify({"status": "error", "message": "Données invalides"}), 400

        results = []
        for candidate in CANDIDATE_DB:
            is_match, reason = match(seeker, candidate)
            if is_match:
                results.append({**candidate, "reason": reason})

        return jsonify(results), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
