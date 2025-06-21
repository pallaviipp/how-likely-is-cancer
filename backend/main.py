from fastapi import FastAPI
from .models import RiskForm
from .scoring import calculate_risk_score
from .database import init_db, get_all_submissions, save_submission


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

    result = calculate_risk_score(data.dict())

    # Make sure this returns something like:
    return {
        "risk_estimate": result["risk_estimate"],
        "contextual_reasons": result["contextual_reasons"],
        "chart_data": result["chart_data"],
        "user_summary": result["user_summary"]
    }
