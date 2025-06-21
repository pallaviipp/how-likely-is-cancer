from fastapi import FastAPI
from .models import RiskForm
from .scoring import calculate_risk_score
from .database import init_db, get_all_submissions, save_submission

app = FastAPI(title="Breast Cancer Risk API")

# Initialize database (create tables etc)
init_db()

@app.get("/")
def root():
    return {"message": "Risk scoring backend is live."}

@app.get("/submissions")
def list_submissions():
    return get_all_submissions()

@app.post("/score")
def score_risk(data: RiskForm):
    # Calculate risk based on validated data model
    result = calculate_risk_score(data.dict())

    # Optionally, save submission to DB
    save_submission(data.dict(), result)

    # Return key results for frontend display
    return {
        "risk_estimate": result["risk_estimate"],
        "risk_percentage": result.get("risk_percentage"),  # add risk %
        "contextual_reasons": result["contextual_reasons"],
        "recommendations": result.get("recommendations", []),  # include recommendations
        "factor_breakdown": result.get("factor_breakdown", {}),
        "chart_data": result["chart_data"],
        "user_summary": result["user_summary"]
    }
