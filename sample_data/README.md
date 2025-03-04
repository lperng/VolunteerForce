# VolunteerForce Sample Data

This directory contains sample CSV files for loading data into Salesforce using Data Loader or other import tools.

## Data Loading Order

When importing these files, it's important to load them in the correct order to maintain referential integrity. Here's the recommended order:

1. **First Load (Objects with no dependencies)**
   - vf_Volunteer__c
   - vf_Staff__c
   - vf_TrainingModule__c
   - vf_Role__c

2. **Second Load (Objects that depend on first load)**
   - vf_Project__c (depends on Staff)
   - vf_Training__c (depends on Volunteer and TrainingModule)
   - vf_Certification__c (depends on Volunteer)
   - vf_RoleTrainingModule__c (depends on Role and TrainingModule)

3. **Third Load (Objects that depend on second load)**
   - vf_Assignment__c (depends on Volunteer and Project)
   - vf_LearningPath__c (depends on Volunteer and Role)
   - vf_VolunteerRole__c (depends on Volunteer and Role)
   - vf_ProjectRole__c (depends on Project and Role)
   - vf_TrainingResource__c (depends on TrainingModule)

4. **Fourth Load (Objects that depend on third load)**
   - vf_Activity__c (depends on Volunteer and Project)
   - vf_Feedback__c (depends on Volunteer and Project)
   - vf_OnboardingChecklist__c (depends on Volunteer, Project, and Role)
   - vf_Recognition__c (depends on Volunteer)
   - vf_BurnoutAssessment__c (depends on Volunteer)
   - vf_ReengagementRecommendation__c (depends on Volunteer)
   - vf_Notification__c (depends on various objects)

## Loading Data Using Salesforce CLI

You can use the Salesforce CLI to load each CSV file into its corresponding custom object. Here are the commands for each file:

### First Load
```bash
sf data import tree -p sample_data/vf_Volunteer__c.csv -s vf_Volunteer__c
sf data import tree -p sample_data/vf_Staff__c.csv -s vf_Staff__c
sf data import tree -p sample_data/vf_TrainingModule__c.csv -s vf_TrainingModule__c
sf data import tree -p sample_data/vf_Role__c.csv -s vf_Role__c
```

### Second Load
```bash
sf data import tree -p sample_data/vf_Project__c.csv -s vf_Project__c
sf data import tree -p sample_data/vf_Training__c.csv -s vf_Training__c
sf data import tree -p sample_data/vf_Certification__c.csv -s vf_Certification__c
sf data import tree -p sample_data/vf_RoleTrainingModule__c.csv -s vf_RoleTrainingModule__c
```

### Third Load
```bash
sf data import tree -p sample_data/vf_Assignment__c.csv -s vf_Assignment__c
sf data import tree -p sample_data/vf_LearningPath__c.csv -s vf_LearningPath__c
sf data import tree -p sample_data/vf_VolunteerRole__c.csv -s vf_VolunteerRole__c
sf data import tree -p sample_data/vf_ProjectRole__c.csv -s vf_ProjectRole__c
sf data import tree -p sample_data/vf_TrainingResource__c.csv -s vf_TrainingResource__c
```

### Fourth Load
```bash
sf data import tree -p sample_data/vf_Activity__c.csv -s vf_Activity__c
sf data import tree -p sample_data/vf_Feedback__c.csv -s vf_Feedback__c
sf data import tree -p sample_data/vf_OnboardingChecklist__c.csv -s vf_OnboardingChecklist__c
sf data import tree -p sample_data/vf_Recognition__c.csv -s vf_Recognition__c
sf data import tree -p sample_data/vf_BurnoutAssessment__c.csv -s vf_BurnoutAssessment__c
sf data import tree -p sample_data/vf_ReengagementRecommendation__c.csv -s vf_ReengagementRecommendation__c
sf data import tree -p sample_data/vf_Notification__c.csv -s vf_Notification__c
```

## Field Types

Special attention should be given to these field types when importing:

1. **JSON Fields** - Many fields contain JSON data (stored as LongTextArea in Salesforce):
   - Skills__c, Interests__c, Availability__c, etc.
   
2. **Lookup Fields** - Reference fields to other objects:
   - Volunteer__c, Project__c, Role__c, etc.
   
3. **Date/DateTime Fields** - Formatted as YYYY-MM-DD:
   - Start_Date__c, End_Date__c, etc.

## Data Loader Settings

When using Salesforce Data Loader, use these settings:

1. Select "Insert" operation
2. Map CSV columns to Salesforce fields by API name
3. Check "Use Bulk API" for large datasets
4. Set "Batch Size" to 200 records

## Notes on External IDs

This sample data is designed to be loaded using Name fields as lookup references. In a production environment, you may want to use External ID fields for better reference handling.