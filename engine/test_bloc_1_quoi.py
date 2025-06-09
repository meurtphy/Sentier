from bloc_1_quoi import bloc_1_quoi

def test_bloc_1_quoi():
    tests = [
        # ✅ Cas 1 : Aucun besoin exprimé
        ({
            "constraints": [],
            "budget_needed": 1000
        }, {
            "engagement": ["financier"],
            "budget_available": 1000
        }, True),

        # ✅ Cas 2 : Financement total
        ({
            "constraints": ["financier"],
            "budget_needed": 1000
        }, {
            "engagement": ["financier"],
            "budget_available": 1000
        }, True),

        # ✅ Cas 3 : Financement partiel (acceptable)
        ({
            "constraints": ["financier"],
            "budget_needed": 1000
        }, {
            "engagement": ["financier"],
            "budget_available": 600
        }, True),

        # ❌ Cas 4 : Financement trop bas
        ({
            "constraints": ["financier"],
            "budget_needed": 1000
        }, {
            "engagement": ["financier"],
            "budget_available": 200
        }, True),  # toujours matché mais toléré

        # ❌ Cas 5 : Aucun besoin couvert
        ({
            "constraints": ["logistique"],
            "budget_needed": 500
        }, {
            "engagement": ["financier"],
            "budget_available": 500
        }, False),

        # ✅ Cas 6 : Besoin partiellement couvert (33%)
        ({
            "constraints": ["logistique", "matériel", "animation"],
            "budget_needed": 0
        }, {
            "engagement": ["logistique"],
            "budget_available": 0
        }, True),

        # ❌ Cas 7 : Besoin trop peu couvert (<33%)
        ({
            "constraints": ["logistique", "matériel", "animation"],
            "budget_needed": 0
        }, {
            "engagement": ["animation"],
            "budget_available": 0
        }, False),
    ]

    for i, (seeker, candidate, expected) in enumerate(tests):
        result, reason = bloc_1_quoi(seeker, candidate)
        status = "✅" if result == expected else "❌"
        print(f"{status} Test {i + 1}: attendu={expected}, obtenu={result} → {reason}")

if __name__ == "__main__":
    test_bloc_1_quoi()
