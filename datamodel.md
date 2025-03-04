# Data Model

The data model is designed to support the three integrated AI agents of VolunteerForce: MatchMaker, OnboardingPro, and RetentionGuard. This comprehensive data structure enables efficient volunteer management throughout the entire lifecycle, from recruitment and matching to onboarding and retention.

## Data Model Overview

This data model addresses the three critical challenges identified in our business proposal:

1. **Inefficient Matching**: The Volunteer, Project, Role, and Assignment entities capture detailed information about skills, interests, availability, and project requirements to enable the MatchMaker Agent to create optimal volunteer-project pairings.

2. **Inconsistent Onboarding**: The TrainingModule, Training, LearningPath, Certification, and OnboardingChecklist entities support the OnboardingPro Agent in delivering personalized training paths and tracking progress.

3. **High Turnover**: The Activity, Feedback, Recognition, BurnoutAssessment, and ReengagementRecommendation entities provide the RetentionGuard Agent with the data needed to monitor engagement patterns, identify burnout risks, and implement retention strategies.

## Agent-Specific Data Support

### MatchMaker Agent
- **Volunteer**: Stores comprehensive profiles including skills, interests, availability, and location
- **Project**: Captures project requirements, schedules, and locations
- **Role**: Defines specific skill requirements for different positions
- **Assignment**: Records the match between volunteers and projects with a match score

### OnboardingPro Agent
- **TrainingModule**: Defines learning content with prerequisites and role requirements
- **Training**: Tracks volunteer progress through modules
- **LearningPath**: Creates personalized training sequences based on roles
- **Certification**: Records qualifications earned by volunteers
- **TrainingResource**: Provides diverse learning materials to accommodate different learning styles
- **OnboardingChecklist**: Ensures consistent onboarding processes across the organization

### RetentionGuard Agent
- **Activity**: Logs volunteer engagement and hours
- **Feedback**: Captures volunteer satisfaction and comments
- **Recognition**: Records achievements and appreciation
- **BurnoutAssessment**: Evaluates volunteer burnout risk with predictive analytics
- **ReengagementRecommendation**: Suggests personalized strategies to re-engage at-risk volunteers

### Supporting Entities
- **Staff**: Manages projects and volunteers
- **Notification**: Facilitates communication across the platform

This data model is designed to be implemented on Salesforce's Agentforce platform, leveraging its powerful CRM capabilities and AI integration to transform volunteer management for nonprofit organizations.

```mermaid
erDiagram
    Volunteer ||--o{ Assignment : "is assigned to"
    Volunteer ||--o{ Training : "completes"
    Volunteer ||--o{ Certification : "earns"
    Volunteer ||--o{ LearningPath : "follows"
    Volunteer ||--o{ Activity : "logs"
    Volunteer ||--o{ Feedback : "provides"
    Volunteer ||--o{ OnboardingChecklist : "completes"
    Volunteer ||--o{ Recognition : "receives"
    Volunteer ||--o{ BurnoutAssessment : "is assessed for"
    
    Project ||--o{ Assignment : "receives"
    Project ||--o{ Role : "requires"
    Project }|--|| Staff : "is managed by"
    
    Role ||--o{ TrainingModule : "requires"
    Role ||--o{ Certification : "requires"
    
    TrainingModule ||--o{ Training : "is completed as"
    TrainingModule ||--o{ TrainingResource : "has"
    
    LearningPath ||--o{ TrainingModule : "includes"
    
    ReengagementRecommendation ||--|| Volunteer : "targets"
    
    Volunteer {
        string id PK
        string name
        jsonb skills
        jsonb interests
        jsonb availability
        date start_date
        string email
        string phone
        float latitude
        float longitude
        string postal_code
        jsonb learning_preferences
    }
    
    Project {
        string id PK
        string name
        string description
        date start_date
        date end_date
        jsonb required_skills
        string manager_id FK
        jsonb schedule
        float latitude
        float longitude
        string postal_code
        jsonb required_resources
    }
    
    Role {
        string id PK
        string name
        string description
        jsonb required_skills
        jsonb recommended_skills
        jsonb required_certifications
    }
    
    Assignment {
        string id PK
        string volunteer_id FK
        string project_id FK
        date start_date
        date end_date
        string status
        float match_score
    }
    
    TrainingModule {
        string id PK
        string name
        string description
        int duration_minutes
        string skill_category
        string difficulty
        jsonb prerequisites
        jsonb required_roles
        jsonb optional_roles
    }
    
    Training {
        string id PK
        string volunteer_id FK
        string module_id FK
        string status
        date completion_date
        float score
    }
    
    LearningPath {
        string id PK
        string volunteer_id FK
        string role_id FK
        date created_date
        int total_modules
        int required_modules
        jsonb modules
    }
    
    TrainingResource {
        string id PK
        string module_id FK
        string name
        string type
        string url
        string learning_style
    }
    
    Certification {
        string id PK
        string volunteer_id FK
        string certification_type
        date issue_date
        date expiration_date
        string status
    }
    
    Activity {
        string id PK
        string volunteer_id FK
        string project_id FK
        date date
        float hours
        string activity_type
        string description
    }
    
    Feedback {
        string id PK
        string volunteer_id FK
        string project_id FK
        date date
        float satisfaction_score
        string comments
    }
    
    OnboardingChecklist {
        string id PK
        string volunteer_id FK
        string project_id FK
        string role_id FK
        date created_date
        string status
        int total_items
        int completed_items
        jsonb items
    }
    
    Recognition {
        string id PK
        string volunteer_id FK
        string type
        string value
        string name
        string description
        date date
    }
    
    BurnoutAssessment {
        string id PK
        string volunteer_id FK
        date assessment_date
        float risk_probability
        string risk_level
        jsonb risk_factors
        jsonb engagement_metrics
        jsonb recommended_strategies
    }
    
    ReengagementRecommendation {
        string id PK
        string volunteer_id FK
        string risk_level
        date creation_date
        jsonb strategies
    }
    
    Staff {
        string id PK
        string name
        string role
        string email
        string phone
    }
    
    Notification {
        string id PK
        string recipient_id
        string recipient_type
        string notification_type
        string subject
        string message
        string action_url
        string priority
        date created_date
        date scheduled_date
        string status
    }
```


