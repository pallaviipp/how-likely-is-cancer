from pydantic import BaseModel
from typing import Optional

class RiskForm(BaseModel):
    symptom: str
    age: int
    gender: str
    location: str
    access_healthcare: str
    age_menarche: int
    age_thelarche: int
    menopause: str
    age_menopause: Optional[int]
    pregnancy: str
    pregnancy_age: Optional[int]
    breastfeeding: str
    pcos: str
    hormonal_use: str
    relatives_with_cancer: int
    brca_known: str
    ethnicity: str
    had_mammo: str
    breast_density: str
    benign_lumps: str
    smoking: str
    alcohol: str
    exercise: str
    anxiety_level: str

