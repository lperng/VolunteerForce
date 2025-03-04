# VolunteerForce Agent API Documentation

Base URL: `http://localhost:8000`

## Authentication

Currently, the API does not require authentication. This should be implemented based on your MCP server's authentication requirements.

## Response Format

All responses are returned in JSON format. Successful responses will contain the requested data, while error responses will include an error message in the following format:

```json
{
    "detail": "Error message description"
}
```

## Common HTTP Status Codes

| Status Code | Description |
|------------|-------------|
| 200 | Successful operation |
| 400 | Bad request - invalid input parameters |
| 404 | Resource not found |
| 500 | Internal server error |

## Endpoints

### OnboardingPro Agent

#### Generate Learning Path

Creates a personalized learning path for a volunteer based on their role.

```http
POST /onboarding/learning-path
```

**Request Body:**
```json
{
    "volunteer_id": "string",
    "role_id": "string"
}
```

**Response:**
```json
{
    "volunteer_id": "string",
    "role_id": "string",
    "learning_path": [
        {
            "module_id": "string",
            "name": "string",
            "description": "string",
            "estimated_duration": "integer",
            "priority": "integer"
        }
    ]
}
```

#### Recommend Resources

Recommends additional learning resources for a specific training module.

```http
POST /onboarding/resources
```

**Request Body:**
```json
{
    "volunteer_id": "string",
    "module_id": "string"
}
```

**Response:**
```json
[
    {
        "resource_id": "string",
        "title": "string",
        "type": "string",
        "url": "string",
        "learning_style": "string"
    }
]
```

#### Verify Certifications

Verifies volunteer certifications and identifies expiring ones.

```http
GET /onboarding/certifications/{volunteer_id}
```

**Response:**
```json
{
    "volunteer_id": "string",
    "valid_certifications": "integer",
    "expiring_certifications": "integer",
    "expired_certifications": "integer",
    "certification_details": {
        "valid": [],
        "expiring": [],
        "expired": []
    }
}
```

### RetentionGuard Agent

#### Predict Burnout Risk

Assesses the burnout risk for a specific volunteer.

```http
GET /retention/burnout-risk/{volunteer_id}
```

**Response:**
```json
{
    "volunteer_id": "string",
    "volunteer_name": "string",
    "assessment_date": "string",
    "risk_probability": "float",
    "risk_level": "string",
    "risk_factors": ["string"],
    "engagement_metrics": {
        "activity_frequency": "float",
        "days_since_last_activity": "integer",
        "weekly_hours": "float",
        "satisfaction_trend": "float"
    },
    "recommended_strategies": ["string"]
}
```

#### Identify Achievements

Identifies volunteer achievements eligible for recognition.

```http
GET /retention/achievements/{volunteer_id}
```

**Response:**
```json
{
    "volunteer_id": "string",
    "achievements": [
        {
            "type": "string",
            "description": "string",
            "date_achieved": "string",
            "metrics": {}
        }
    ]
}
```

#### Suggest Reengagement Strategies

Suggests personalized reengagement strategies for a volunteer.

```http
POST /retention/reengagement
```

**Request Body:**
```json
{
    "volunteer_id": "string",
    "risk_level": "string" // optional
}
```

**Response:**
```json
{
    "volunteer_id": "string",
    "strategies": [
        {
            "type": "string",
            "description": "string",
            "priority": "string",
            "action_items": ["string"]
        }
    ]
}
```

### MatchMaker Agent

#### Find Matches

Finds best matching projects for a specific volunteer.

```http
POST /matchmaker/matches
```

**Request Body:**
```json
{
    "volunteer_id": "string",
    "top_n": "integer" // optional
}
```

**Response:**
```json
[
    {
        "project_id": "string",
        "project_name": "string",
        "overall_score": "float",
        "skill_match": "float",
        "availability_match": "float",
        "location_match": "float"
    }
]
```

#### Schedule Assignment

Schedules a volunteer for a project.

```http
POST /matchmaker/schedule
```

**Request Body:**
```json
{
    "volunteer_id": "string",
    "project_id": "string"
}
```

**Response:**
```json
{
    "success": "boolean",
    "assignment_id": "string",
    "match_score": {
        "overall_score": "float",
        "skill_match": "float",
        "availability_match": "float",
        "location_match": "float"
    }
}
```

### Health Check

Check the API server's health status.

```http
GET /health
```

**Response:**
```json
{
    "status": "string",
    "version": "string"
}
```

## Code Examples

### Python

```python
import requests

base_url = "http://localhost:8000"

# Generate learning path
def generate_learning_path(volunteer_id: str, role_id: str):
    response = requests.post(
        f"{base_url}/onboarding/learning-path",
        json={
            "volunteer_id": volunteer_id,
            "role_id": role_id
        }
    )
    return response.json()

# Check burnout risk
def get_burnout_risk(volunteer_id: str):
    response = requests.get(f"{base_url}/retention/burnout-risk/{volunteer_id}")
    return response.json()

# Find matches with top N limit
def find_matches(volunteer_id: str, top_n: int = 5):
    response = requests.post(
        f"{base_url}/matchmaker/matches",
        json={
            "volunteer_id": volunteer_id,
            "top_n": top_n
        }
    )
    return response.json()
```

### cURL

```bash
# Generate learning path
curl -X POST http://localhost:8000/onboarding/learning-path \
    -H "Content-Type: application/json" \
    -d '{"volunteer_id": "V123", "role_id": "R456"}'

# Check burnout risk
curl http://localhost:8000/retention/burnout-risk/V123

# Find matches
curl -X POST http://localhost:8000/matchmaker/matches \
    -H "Content-Type: application/json" \
    -d '{"volunteer_id": "V123", "top_n": 5}'
```

## Error Handling

All endpoints follow consistent error handling patterns. Here are some common error scenarios:

### Resource Not Found
```json
{
    "detail": "Volunteer not found"
}
```

### Invalid Input
```json
{
    "detail": "Invalid volunteer_id format"
}
```

### Server Error
```json
{
    "detail": "Internal server error occurred"
}
```

## Rate Limiting

Currently, there are no rate limits implemented. Consider adding rate limiting based on your MCP server's requirements. 