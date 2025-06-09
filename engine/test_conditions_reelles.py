from match import match

# Cas réel simulé
scenarios = [
    {
        "seeker": {
            "constraints": ["hébergement", "aide alimentaire", "financier"],
            "budget_needed": 300,
        },
        "candidate": {
            "engagement": ["hébergement", "logistique", "financier"],
            "budget_available": 150,
        },
        "expected": True  # On tolère un financement partiel + au moins 1 besoin couvert
    },
    {
        "seeker": {
            "constraints": ["mobilité", "logement"],
            "budget_needed": 0,
        },
        "candidate": {
            "engagement": ["inclusion numérique", "logistique"],
            "budget_available": 0,
        },
        "expected": False  # Aucun besoin couvert
    },
    # Ajoute d’autres cas limites : recouvrement flou, format bizarre, budget incohérent, etc.
]

for i, s in enumerate(scenarios):
    res, reason = match(s["seeker"], s["candidate"])
    expected = s["expected"]
    status = "✅" if res == expected else "❌"
    print(f"{status} Test {i+1}: attendu={expected}, obtenu={res} → {reason}")
