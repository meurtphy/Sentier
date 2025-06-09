import requests
from geopy.distance import geodesic

def geocode_city(city_name):
    """
    Utilise l’API Nominatim pour récupérer la lat/lon et le label.
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": city_name, "format": "json", "limit": 1}
    headers = {"User-Agent": "SentierBot/1.0"}
    try:
        res = requests.get(url, params=params, headers=headers)
        res.raise_for_status()
        data = res.json()
        if data:
            return {
                "lat": float(data[0]["lat"]),
                "lon": float(data[0]["lon"]),
                "label": data[0]["display_name"]
            }
        else:
            return None
    except Exception as e:
        print("Erreur géocodage :", e)
        return None

def extract_geo_scope(label):
    """
    Extrait la ville, région, pays à partir du label Nominatim.
    """
    parts = [p.strip() for p in label.split(",")]
    city = parts[0] if len(parts) > 0 else ""
    region = parts[2] if len(parts) > 2 else ""
    country = parts[-1] if parts else ""
    return {"city": city, "region": region, "country": country}

def distance_km(pos1, pos2):
    return geodesic((pos1["lat"], pos1["lon"]), (pos2["lat"], pos2["lon"])).km

def bloc_2_zone(seeker, candidate):
    """
    Bloc 2 – OÙ (Z → A) : Vérifie que le lieu d’action du candidate couvre celui du seeker,
    en utilisant les vraies coordonnées géographiques.
    """
    seeker_zone = seeker.get("zone", "")
    candidate_zone = candidate.get("zone", "")

    geo_s = geocode_city(seeker_zone)
    geo_c = geocode_city(candidate_zone)

    if not geo_s or not geo_c:
        return False, "OÙ : Géolocalisation échouée"

    scope_s = extract_geo_scope(geo_s["label"])
    scope_c = extract_geo_scope(geo_c["label"])

    # Vérifier que les deux sont en France (évite les erreurs frontalières comme Genève)
    if "france" not in scope_s["country"].lower() or "france" not in scope_c["country"].lower():
        return False, "OÙ : Un des profils est hors de France"

    # Calcul de la distance entre les deux
    distance = distance_km(geo_s, geo_c)

    # Cas 1 : Local (< 50 km)
    if distance <= 50:
        return True, f"OÙ : Couverture locale ({distance:.0f} km)"

    # Cas 2 : Régional (≤ 200 km)
    if distance <= 200:
        return True, f"OÙ : Couverture régionale ({distance:.0f} km)"

    # Cas 3 : National = tout France
    if candidate_zone.lower() == "national":
        return True, f"OÙ : Couverture nationale (France entière)"

    # Sinon, trop éloigné
    return False, f"OÙ : Distance trop grande ({distance:.0f} km > 200 km)"
