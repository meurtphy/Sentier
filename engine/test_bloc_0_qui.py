from bloc_O_qui import bloc_0_respect_besoin

def run_test(label, seeker, candidate, expected):
    result, reason = bloc_0_respect_besoin(seeker, candidate)
    success = result == expected
    emoji = "✅" if success else "❌"
    print(f"{emoji} {label}: attendu={expected}, obtenu={result} → {reason}")

if __name__ == "__main__":
    print("\n🔍 Tests bloc_0_respect_besoin :")

    # Test 1 – Match explicite parfait
    run_test("Test 1",
        {"type": "association", "target": ["entreprise"]},
        {"type": "entreprise", "target": ["association"]},
        True
    )

    # Test 2 – Match implicite (asso sans target → default = entreprise)
    run_test("Test 2",
        {"type": "association"},
        {"type": "entreprise", "target": ["association"]},
        True
    )

    # Test 3 – Types mal orthographiés
    run_test("Test 3",
        {"type": "assos", "target": ["entreprises"]},
        {"type": "societe", "target": ["asso"]},
        True
    )

    # Test 4 – Entreprise vise tous, asso vise entreprise
    run_test("Test 4",
        {"type": "association", "target": ["entreprise"]},
        {"type": "entreprise", "target": ["tous"]},
        True
    )

    # Test 5 – Asso vise personne (erreur logique)
    run_test("Test 5",
        {"type": "association", "target": []},
        {"type": "entreprise", "target": ["association"]},
        True  # Accepté car défaut = ["entreprise"]

    )

    # Test 6 – Manque type chez l’un
    run_test("Test 6",
        {"target": ["entreprise"]},
        {"type": "entreprise", "target": ["association"]},
        False
    )

    # Test 7 – Auto-match (entreprise ↔ entreprise autorisé)
    run_test("Test 7",
        {"type": "entreprise", "target": ["entreprise"]},
        {"type": "entreprise", "target": ["entreprise"]},
        True
    )

    # Test 8 – Aucun ne vise l'autre
    run_test("Test 8",
        {"type": "association", "target": ["association"]},
        {"type": "entreprise", "target": ["entreprise"]},
        False
    )
