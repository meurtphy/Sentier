from match import match

def test_match():
    tests = [

        # ❌ Cas 1 – Candidat = association qui cherche, Seeker = entreprise qui cherche aussi → inversion
        ({
            "type": "entreprise",
            "wants": "recevoir",
            "constraints": ["financier"],
            "budget_needed": 5000,
            "zone": "Toulouse",
            "disponibilité": "2024-10-01"
        }, {
            "type": "association",
            "wants": "recevoir",
            "engagement": ["financier"],
            "budget_available": 3000,
            "zone": "Toulouse",
            "disponibilité": "2024-10-01"
        }, "NON"),

        # ❌ Cas 2 – Tout est compatible sauf la zone (Toulouse vs Lille)
        ({
            "type": "association",
            "wants": "recevoir",
            "constraints": ["logistique"],
            "zone": "Toulouse",
            "budget_needed": 0,
            "disponibilité": "2024-12-01"
        }, {
            "type": "entreprise",
            "wants": "donner",
            "engagement": ["logistique"],
            "zone": "Lille",
            "budget_available": 0,
            "disponibilité": "2024-12-01"
        }, "NON"),

        # ✅ Cas 3 – Profil sans besoin exprimé (toléré), mais tout le reste est bon
        ({
            "type": "association",
            "wants": "recevoir",
            "constraints": [],
            "budget_needed": 0,
            "zone": "national",
            "disponibilité": "2024-09-01"
        }, {
            "type": "entreprise",
            "wants": "donner",
            "engagement": ["logistique", "animation"],
            "budget_available": 0,
            "zone": "national",
            "disponibilité": "2024-09-01"
        }, "MATCH"),

        # ❌ Cas 4 – Match parfait sauf dates incompatibles
        ({
            "type": "association",
            "wants": "recevoir",
            "constraints": ["animation"],
            "budget_needed": 0,
            "zone": "Lyon",
            "disponibilité": "2025-01-01"
        }, {
            "type": "entreprise",
            "wants": "donner",
            "engagement": ["animation"],
            "budget_available": 0,
            "zone": "Lyon",
            "disponibilité": "2023-12-01"
        }, "NON"),
    ]

    for i, (seeker, candidate, expected_result) in enumerate(tests):
        result, reason = match(seeker, candidate)
        status = "✅" if result == expected_result else "❌"
        print(f"{status} Test {i + 1}: attendu={expected_result}, obtenu={result} → {reason}")

if __name__ == "__main__":
    test_match()
