from datetime import datetime, timedelta

def parse_date_range(date_str):
    """
    Gère les dates uniques ou plages de type "2024-09-01 to 2024-09-30"
    """
    if "to" in date_str:
        parts = date_str.split("to")
        try:
            start = datetime.strptime(parts[0].strip(), "%Y-%m-%d")
            end = datetime.strptime(parts[1].strip(), "%Y-%m-%d")
            return start, end
        except:
            return None, None
    else:
        try:
            date = datetime.strptime(date_str.strip(), "%Y-%m-%d")
            return date, date
        except:
            return None, None

def bloc_3_quand(seeker, candidate, tolerance_days=30):
    """
    Bloc 3 – QUAND (Z → A) :
    Vérifie que le délai ou la temporalité de l'action permet que le match ait lieu.
    Accepte dates ou mots-clés.
    """
    seeker_when = seeker.get("when", "").lower()
    candidate_when = candidate.get("when", "").lower()

    # Cas manquants
    if not seeker_when or not candidate_when:
        return True, "QUAND : Données manquantes — tolérées"

    # Cas flexibles
    if "flexible" in seeker_when or "flexible" in candidate_when:
        return True, "QUAND : Flexible → accepté"

    # Mapping textuel
    mapping = {
        "immédiat": 0,
        "urgent": 7,
        "3 mois": 90,
        "6 mois": 180,
        "12 mois": 365
    }

    if seeker_when in mapping and candidate_when in mapping:
        s_delay = mapping[seeker_when]
        c_delay = mapping[candidate_when]
        if c_delay <= s_delay + tolerance_days:
            return True, f"QUAND : {candidate_when} compatible avec {seeker_when}"
        else:
            return False, f"QUAND : Délai trop long ({candidate_when} > {seeker_when})"

    # Essai avec dates exactes
    seeker_start, seeker_end = parse_date_range(seeker_when)
    candidate_start, candidate_end = parse_date_range(candidate_when)

    if seeker_start and candidate_start:
        latest_start = max(seeker_start, candidate_start)
        earliest_end = min(seeker_end, candidate_end)
        delta = (latest_start - seeker_start).days

        if latest_start <= seeker_end and delta <= tolerance_days:
            return True, f"QUAND : Périodes compatibles ({seeker_when} vs {candidate_when})"
        else:
            return False, f"QUAND : Décalage trop grand ou pas de recouvrement ({seeker_when} vs {candidate_when})"

    return True, "QUAND : Format non reconnu, toléré par défaut"
