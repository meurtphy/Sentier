from bloc_O_qui import bloc_0_respect_besoin
from bloc_1_quoi import bloc_1_quoi
from bloc_2_ou import bloc_2_zone
from bloc_3_quand import bloc_3_quand

def match(seeker, candidate):
    """
    Moteur central d'appariement Z → A.
    Chaque bloc valide ou non une condition essentielle.
    Retourne ("MATCH"/"NON", justification textuelle complète)
    """

    reasons = []

    # Bloc 0 — QUI : intentions compatibles ?
    ok, reason = bloc_0_respect_besoin(seeker, candidate)
    reasons.append(f"QUI : {reason}")
    if not ok:
        return "NON", "Refusé au bloc QUI → " + reason

    # Bloc 1 — QUOI : compatibilité besoin / offre
    ok, reason = bloc_1_quoi(seeker, candidate)
    reasons.append(f"QUOI : {reason}")
    if not ok:
        return "NON", "Refusé au bloc QUOI → " + reason

    # Bloc 2 — OÙ : compatibilité géographique
    ok, reason = bloc_2_zone(seeker, candidate)
    reasons.append(f"OÙ : {reason}")
    if not ok:
        return "NON", "Refusé au bloc OÙ → " + reason

    # Bloc 3 — QUAND : compatibilité temporelle (optionnel)
    ok, reason = bloc_3_quand(seeker, candidate)
    reasons.append(f"QUAND : {reason}")
    if not ok:
        return "NON", "Refusé au bloc QUAND → " + reason

    # Tous validés
    return "MATCH", "✔ Tous les blocs validés :\n- " + "\n- ".join(reasons)
