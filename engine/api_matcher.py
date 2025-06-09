from fastapi import FastAPI
from pydantic import BaseModel
from yaml_engine import load_rules, evaluate_rules

app = FastAPI(title="Picser Matchmaking API")
rules = load_rules("tree_rules.yaml")

# Modèle d'entrée : les features nécessaires
class MatchRequest(BaseModel):
    budget_ratio: float
    zone_match: float
    has_finance_offer: float
    has_finance_need: float
    need_overlap_ratio: float
    need_overlap_count: float

@app.post("/match")
def match_logic(request: MatchRequest):
    input_data = request.dict()
    result = evaluate_rules(rules, input_data)
    return {
        "input": input_data,
        "match": result
    }
