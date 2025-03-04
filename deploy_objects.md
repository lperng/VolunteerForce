# VolunteerForce Custom Object Deployment Guide

This guide explains how to deploy the VolunteerForce custom objects to your Salesforce org.

## Prerequisites

1. Ensure you have the Salesforce CLI installed
   ```bash
   sf --version
   ```
   If not installed, follow the instructions in `sfdx.md`

2. Authenticate to your Salesforce org
   ```bash
   # For sandbox
   sf org login web --instance-url https://test.salesforce.com --alias volunteerforce-sandbox
   
   # For production
   sf org login web --instance-url https://login.salesforce.com --alias volunteerforce-prod
   ```

## Custom Objects Overview

The following custom objects have been created:

1. **vf_Volunteer__c** - Stores volunteer information and attributes
2. **vf_Project__c** - Stores project information and requirements
3. **vf_Staff__c** - Stores staff member information
4. **vf_Assignment__c** - Maps volunteers to projects
5. **vf_Role__c** - Defines role types with required skills and certifications
6. **vf_TrainingModule__c** - Stores training modules with difficulty levels
7. **vf_Training__c** - Tracks a volunteer's progress on specific training modules
8. **vf_Certification__c** - Records certifications earned by volunteers
9. **vf_LearningPath__c** - Defines personalized learning paths for roles
10. **vf_Activity__c** - Logs volunteer activities and hours
11. **vf_Feedback__c** - Captures volunteer feedback with satisfaction scores
12. **vf_OnboardingChecklist__c** - Tracks volunteer onboarding progress
13. **vf_Recognition__c** - Stores awards and recognition for volunteers
14. **vf_BurnoutAssessment__c** - Records assessments of volunteer burnout risk
15. **vf_TrainingResource__c** - Contains resources for training modules
16. **vf_ReengagementRecommendation__c** - Suggests strategies for reengaging volunteers
17. **vf_Notification__c** - Manages notifications for volunteers and staff

### Junction Objects (Many-to-Many Relationships)

18. **vf_VolunteerRole__c** - Connects volunteers to roles
19. **vf_RoleTrainingModule__c** - Connects roles to training modules
20. **vf_ProjectRole__c** - Connects projects to roles

## Deployment Steps

1. Deploy all custom objects at once
   ```bash
   sf project deploy start --source-dir force-app/main/default/objects
   ```

2. Deploy package (objects, classes and flows)
   ```bash
   sf project deploy start --manifest force-app/package.xml
   ```

3. Validate deployment without actually deploying (optional)
   ```bash
   sf project deploy start --source-dir force-app/main/default/objects --dry-run
   ```

## Verification

After deployment, verify that the objects were created correctly:

1. Check for deployment errors
   ```bash
   sf project deploy report
   ```

2. Use the Salesforce Setup menu to navigate to:
   - Setup > Object Manager > vf_Volunteer__c
   - Setup > Object Manager > vf_Project__c
   - Setup > Object Manager > vf_Staff__c
   - Setup > Object Manager > vf_Assignment__c

## Important Notes

1. These objects were created with the "vf_" prefix to avoid naming conflicts with existing objects in your org
2. Each object has been configured with appropriate relationship fields to maintain referential integrity
3. JSON data is stored in long text fields with a 32,768 character limit

## Post-Deployment Tasks

1. Create custom tabs for each object
2. Setup page layouts
3. Configure field-level security
4. Setup list views