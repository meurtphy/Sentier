import yaml

def load_rules(filepath="tree_rules.yaml"):
    with open(filepath, "r") as f:
        lines = f.readlines()

    rules = []
    stack = []

    for line in lines:
        if line.strip().startswith("#") or not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        content = line.strip()[2:]  # remove "- "
        node = {"depth": indent // 2, "content": content}
        rules.append(node)

    return rules

def evaluate_rules(rules, input_data):
    pointer = 0
    depth = 0

    while pointer < len(rules):
        node = rules[pointer]
        if node["depth"] < depth:
            return None  # remonte trop haut → invalide
        if node["content"].startswith("class:"):
            return node["content"].split(":")[1].strip() == "True"

        # Traitement condition
        condition = node["content"]
        parts = condition.split()
        if len(parts) != 3:
            return None

        var, op, val = parts
        try:
            val = float(val)
            var_value = float(input_data.get(var, 0))
        except:
            return None

        match = False
        if op == "<=" and var_value <= val:
            match = True
        elif op == ">" and var_value > val:
            match = True

        # si la condition est remplie, continuer sur les fils à +1 niveau
        pointer += 1
        depth = node["depth"] + 1

        # sinon, sauter toutes les lignes enfants
        if not match:
            while pointer < len(rules) and rules[pointer]["depth"] > node["depth"]:
                pointer += 1

    return None  # rien trouvé

# Exemple d’usage
if __name__ == "__main__":
    rules = load_rules("tree_rules.yaml")

    test_input = {
        "budget_ratio": 0.45,
        "zone_match": 1.0,
        "has_finance_offer": 1.0,
        "has_finance_need": 1.0,
        "need_overlap_ratio": 0.5,
        "need_overlap_count": 1
    }

    result = evaluate_rules(rules, test_input)
    print(f"✅ Résultat logique : MATCH = {result}")
