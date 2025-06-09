from flask import Flask, request, jsonify
import logging
import re
import json
from typing import Dict

import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)


def _scrape_company_html(slug: str) -> Dict:
    """Scrape company info from annuaire-entreprises page."""
    url = f"https://annuaire-entreprises.data.gouv.fr/entreprise/{slug}"
    logging.info("scraping HTML %s", url)
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    script = soup.find("script", id="__NEXT_DATA__")
    if not script or not script.string:
        raise ValueError("no data found in page")
    data = json.loads(script.string)
    info = data.get("props", {}).get("pageProps", {})
    for key in ("entreprise", "enterprise", "etablissement"):
        if isinstance(info.get(key), dict):
            return info[key]
    return info


def _fetch_company_info(query: str) -> dict:
    """Lookup a company by name, SIREN or SIRET.

    This tries the official API when a numeric identifier is provided.
    For text queries, it first scrapes the public web page and falls back
    to the SIRENE search API if scraping fails.
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
        try:
            return _scrape_company_html(norm)
        except Exception:
            logging.exception("HTML scrape failed, fallback to API")
            url = "https://entreprise.data.gouv.fr/api/sirene/v3/unites_legales"
            resp = requests.get(
                url,
                params={"nom_raison_sociale": query, "per_page": 1},
                timeout=10,
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
