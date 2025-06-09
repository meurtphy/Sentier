from bloc_3_quand import bloc_3_quand

def test(desc, seeker, candidate, expected):
    result, reason = bloc_3_quand(seeker, candidate)
    ok = result == expected
    emoji = "✅" if ok else "❌"
    print(f"{emoji} {desc}: attendu={expected}, obtenu={result} → {reason}")

if __name__ == "__main__":
    print("\n🔍 Tests bloc_3_quand :\n")

    test("Test 1: urgent vs 3 mois (doit échouer)",
         {"when": "urgent"}, {"when": "3 mois"}, False)

    test("Test 2: 3 mois vs urgent (doit passer)",
         {"when": "3 mois"}, {"when": "urgent"}, True)

    test("Test 3: flexible toléré",
         {"when": "urgent"}, {"when": "flexible"}, True)

    test("Test 4: données manquantes",
         {"when": ""}, {"when": ""}, True)

    test("Test 5: date vs plage — incompatible",
         {"when": "2024-09-01"}, {"when": "2024-09-15 to 2024-10-01"}, False)

    test("Test 6: date vs date éloignée",
         {"when": "2024-09-01"}, {"when": "2024-11-01"}, False)

    test("Test 7: date vs date identique",
         {"when": "2024-09-01"}, {"when": "2024-09-01"}, True)

    test("Test 8: plages compatibles",
         {"when": "2024-09-01 to 2024-09-30"}, {"when": "2024-09-15 to 2024-10-15"}, True)

    test("Test 9: plages non compatibles",
         {"when": "2024-09-01 to 2024-09-30"}, {"when": "2024-10-15 to 2024-11-01"}, False)

    test("Test 10: format inconnu",
         {"when": "quand tu veux"}, {"when": "bientôt"}, True)
