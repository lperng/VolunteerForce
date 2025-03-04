# Data Model

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


