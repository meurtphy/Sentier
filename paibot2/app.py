from flask import Flask, request, jsonify
import logging
import re
import requests

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)


def _fetch_company_info(query: str) -> dict:
    """Lookup a company by name, SIREN or SIRET using the
    entreprise.data.gouv.fr API.
    """
    norm = re.sub(r"\s+", "", query)
    if re.fullmatch(r"\d{14}", norm):
        url = f"https://entreprise.data.gouv.fr/api/sirene/v3/etablissements/{norm}"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.json().get("etablissement", {})
    elif re.fullmatch(r"\d{9}", norm):
        url = f"https://entreprise.data.gouv.fr/api/sirene/v3/unites_legales/{norm}"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.json().get("unite_legale", {})
    else:
        url = "https://entreprise.data.gouv.fr/api/sirene/v3/unites_legales"
        resp = requests.get(
            url, params={"nom_raison_sociale": query, "per_page": 1}, timeout=10
        )
        resp.raise_for_status()
        items = resp.json().get("unites_legales") or []
        if not items:
            raise ValueError("not found")
        return items[0]


@app.post("/scrape")
def scrape():
    data = request.get_json(force=True) or {}
    query = data.get("query") or data.get("url") or ""
    if not query:
        return jsonify({"error": "query required"}), 400

    logging.info("/scrape query=%s", query)

    try:
        info = _fetch_company_info(query)

        addr_parts = [
            info.get("numero_voie"),
            info.get("type_voie"),
            info.get("libelle_voie"),
            info.get("code_postal"),
            info.get("libelle_commune"),
        ]

        result = {
            "siret": info.get("siret")
            or info.get("siret_siege")
            or info.get("etablissement_siege", {}).get("siret"),
            "siren": info.get("siren"),
            "naf_ape": info.get("activite_principale"),
            "raison_sociale": info.get("denomination")
            or info.get("nom_raison_sociale"),
            "adresse_siege": " ".join([p for p in addr_parts if p]),
            "source_query": query,
        }

        logging.info("/scrape result for query=%s -> %s", query, result)
        return jsonify(result)
    except Exception as exc:
        logging.exception("lookup failed for query=%s", query)
        return (
            jsonify({"error": "lookup_failed", "detail": str(exc), "query": query}),
            502,
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
