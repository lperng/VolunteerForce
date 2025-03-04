from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from onboardingpro import OnboardingProAgent
from retentionguard import RetentionGuardAgent
from matchmaker import MatchMakerAgent

app = FastAPI(
    title="VolunteerForce Agent API",
    description="API endpoints for VolunteerForce's intelligent agents",
    version="1.0.0"
)

# Initialize agents (you'll need to provide proper connections)
sf_connection = None  # Replace with actual Salesforce connection
lms_connection = None  # Replace with actual LMS connection

onboarding_agent = OnboardingProAgent(sf_connection, lms_connection)
retention_agent = RetentionGuardAgent(sf_connection)
matchmaker_agent = MatchMakerAgent(sf_connection)

# Pydantic models for request/response validation
class LearningPathRequest(BaseModel):
    volunteer_id: str
    role_id: str

class ResourceRequest(BaseModel):
    volunteer_id: str
    module_id: str

class MatchRequest(BaseModel):
    volunteer_id: str
    top_n: Optional[int] = None

class AssignmentRequest(BaseModel):
    volunteer_id: str
    project_id: str

class ReengagementRequest(BaseModel):
    volunteer_id: str
    risk_level: Optional[str] = None

# OnboardingPro Agent endpoints
@app.post("/onboarding/learning-path", tags=["OnboardingPro"])
async def generate_learning_path(request: LearningPathRequest):
    try:
        result = onboarding_agent.generate_learning_path(
            request.volunteer_id,
            request.role_id
        )
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/onboarding/resources", tags=["OnboardingPro"])
async def recommend_resources(request: ResourceRequest):
    try:
        result = onboarding_agent.recommend_resources(
            request.volunteer_id,
            request.module_id
        )
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/onboarding/certifications/{volunteer_id}", tags=["OnboardingPro"])
async def verify_certifications(volunteer_id: str):
    try:
        result = onboarding_agent.verify_certifications(volunteer_id)
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# RetentionGuard Agent endpoints
@app.get("/retention/burnout-risk/{volunteer_id}", tags=["RetentionGuard"])
async def predict_burnout_risk(volunteer_id: str):
    try:
        result = retention_agent.predict_burnout_risk(volunteer_id)
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/retention/achievements/{volunteer_id}", tags=["RetentionGuard"])
async def identify_achievements(volunteer_id: str):
    try:
        result = retention_agent.identify_achievements(volunteer_id)
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/retention/reengagement", tags=["RetentionGuard"])
async def suggest_reengagement_strategies(request: ReengagementRequest):
    try:
        result = retention_agent.suggest_reengagement_strategies(
            request.volunteer_id,
            request.risk_level
        )
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# MatchMaker Agent endpoints
@app.post("/matchmaker/matches", tags=["MatchMaker"])
async def find_matches(request: MatchRequest):
    try:
        result = matchmaker_agent.find_matches_for_volunteer(
            request.volunteer_id,
            request.top_n
        )
        if not result:
            raise HTTPException(status_code=404, detail="No matches found")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/matchmaker/schedule", tags=["MatchMaker"])
async def schedule_assignment(request: AssignmentRequest):
    try:
        result = matchmaker_agent.schedule_assignment(
            request.volunteer_id,
            request.project_id
        )
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 