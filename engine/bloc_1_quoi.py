def bloc_1_quoi(seeker, candidate):
    """
    Bloc 1 – QUOI (Z → A) : Vérifie si les besoins du seeker sont couverts
    par les engagements du candidate. Intègre logique de budget partiel,
    recouvrement partiel et bonus financier. Autorise une tolérance minimale.
    """

    def normalize(term):
        return term.strip().lower()

    seeker_constraints = [normalize(c) for c in seeker.get("constraints", [])]
    candidate_engagements = [normalize(e) for e in candidate.get("engagement", [])]
    seeker_budget = seeker.get("budget_needed", 0)
    candidate_budget = candidate.get("budget_available", 0)

    # Cas 1 : Aucun besoin exprimé
    if not seeker_constraints:
        return True, "QUOI : Aucun besoin exprimé → match possible mais non prioritaire (profil flou)"

    # Cas 2 : Besoins couverts (partiellement ou totalement)
    covered = []
    for need in seeker_constraints:
        if any(need in engagement or engagement in need for engagement in candidate_engagements):
            covered.append(need)

    overlap_ratio = len(covered) / len(seeker_constraints)

    # Cas 2a : Aucun besoin couvert
    if not covered:
        return False, f"QUOI : Aucun besoin couvert — besoins demandés : {seeker_constraints}, engagements proposés : {candidate_engagements}"

    # Cas 2b : Besoin financier inclus
    if "financier" in seeker_constraints and "financier" in candidate_engagements:
        if candidate_budget >= seeker_budget:
            return True, "QUOI : Financement total + type compatible"
        elif candidate_budget >= 0.5 * seeker_budget:
            return True, "QUOI : Financement partiel acceptable (≥ 50%)"
        else:
            return True, "QUOI : Financement très partiel mais engagement correct (match toléré)"

    # Cas 2c : Recouvrement partiel d'autres besoins
    if overlap_ratio >= 0.33:
        return True, f"QUOI : Besoins partiellement couverts ({', '.join(covered)})"
    elif overlap_ratio >= 0.2:
        return True, f"QUOI : Recouvrement très faible mais non nul ({', '.join(covered)})"

    return False, f"QUOI : Trop peu de besoins couverts ({', '.join(covered)} — {len(covered)} sur {len(seeker_constraints)})"
