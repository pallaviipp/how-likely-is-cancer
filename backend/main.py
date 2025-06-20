from fastapi import FastAPI
from models import RiskForm
from scoring import calculate_risk_score
from database import init_db, get_all_submissions, save_submission


app = FastAPI()
init_db()


@app.get("/")
def root():
    return {"message": "Risk scoring backend is live."}
    
@app.get("/submissions")
def list_submissions():
    return get_all_submissions()


@app.post("/score")
def score_risk(data: RiskForm):
    user_dict = data.dict()
    result = calculate_risk_score(user_dict)
    save_submission(user_dict, result["risk_estimate"])
    return result

