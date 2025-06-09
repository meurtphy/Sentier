def bloc_0_respect_besoin(seeker, candidate):
    print("✅ bloc_O_qui activé")

def bloc_0_respect_besoin(seeker, candidate):
    """
    Bloc O – QUI (Z → A) : Vérifie que chacun accepte explicitement de matcher avec l'autre.
    On tolère le flou ou l'absence de données si d'autres blocs compensent.
    """
    seeker_target = seeker.get("target", [])
    candidate_target = candidate.get("target", [])
    seeker_type = seeker.get("type", "")
    candidate_type = candidate.get("type", "")

    if not seeker_target and not candidate_target:
        return True, "Z toléré : aucune cible définie (double flou)"

    if not seeker_type and not candidate_type:
        return True, "Z toléré : aucun type renseigné (double flou)"

    seeker_ok = candidate_type in seeker_target or "tous" in seeker_target if seeker_target else True
    candidate_ok = seeker_type in candidate_target or "tous" in candidate_target if candidate_target else True

    if seeker_ok and candidate_ok:
        return True, "Z validé : intention explicite ou implicite"
    else:
        return False, "Z refusé : au moins un des deux ne cible pas l'autre"