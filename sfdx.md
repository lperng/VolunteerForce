# VolunteerForce SFDX Deployment Guide

This guide explains how to deploy the VolunteerForce components to your Salesforce org using SFDX CLI commands.

## Prerequisites

1. Install Salesforce CLI
```bash
# macOS
brew install sf-cli

# Windows (using PowerShell)
Set-ExecutionPolicy RemoteSigned
iex "& { $(irm https://developer.salesforce.com/media/salesforce-cli/sf/channels/stable/sf-install.ps1) }"

# Linux
wget https://developer.salesforce.com/media/salesforce-cli/sf/channels/stable/sf-linux-x64.tar.gz
tar xzf sf-linux-x64.tar.gz
./sf/install
```

2. Verify installation
```bash
sf --version
```

## Project Setup

1. Create a new SFDX project (if not already created)
```bash
sf project create --name VolunteerForce --template standard
cd VolunteerForce
```

2. Create project structure
```bash
mkdir -p force-app/main/default/classes
mkdir -p force-app/main/default/flows
mkdir -p force-app/main/default/objects
```

## Authentication

1. Connect to your Salesforce org

For a sandbox:
```bash
sf org login web --instance-url https://test.salesforce.com --alias volunteerforce-sandbox
```

For production:
```bash
sf org login web --instance-url https://login.salesforce.com --alias volunteerforce-prod
```

2. Set as default org (optional)
```bash
sf config set target-org volunteerforce-sandbox
```

## Deployment

1. Deploy all components
```bash
sf project deploy start --source-dir force-app
```

2. Deploy specific components

Deploy Apex classes only:
```bash
sf project deploy start --source-dir force-app/main/default/classes
```

Deploy flows only:
```bash
sf project deploy start --source-dir force-app/main/default/flows
```

Deploy custom objects only:
```bash
sf project deploy start --source-dir force-app/main/default/objects
```

3. Check deployment status
```bash
sf project deploy report
```

## Custom Objects Deployment

### Deploy All Custom Objects

Deploy all custom objects at once:
```bash
sf project deploy start --source-dir force-app/main/default/objects
```

### Deploy Individual Custom Objects

You can deploy specific custom objects as needed:

```bash
# First batch - Objects with no dependencies
sf project deploy start --source-dir force-app/main/default/objects/vf_Volunteer__c
sf project deploy start --source-dir force-app/main/default/objects/vf_Staff__c
sf project deploy start --source-dir force-app/main/default/objects/vf_TrainingModule__c
sf project deploy start --source-dir force-app/main/default/objects/vf_Role__c

# Second batch - Objects that depend on first batch
sf project deploy start --source-dir force-app/main/default/objects/vf_Project__c
sf project deploy start --source-dir force-app/main/default/objects/vf_Training__c
sf project deploy start --source-dir force-app/main/default/objects/vf_Certification__c
sf project deploy start --source-dir force-app/main/default/objects/vf_RoleTrainingModule__c

# Third batch - Objects that depend on second batch
sf project deploy start --source-dir force-app/main/default/objects/vf_Assignment__c
sf project deploy start --source-dir force-app/main/default/objects/vf_LearningPath__c
sf project deploy start --source-dir force-app/main/default/objects/vf_VolunteerRole__c
sf project deploy start --source-dir force-app/main/default/objects/vf_ProjectRole__c
sf project deploy start --source-dir force-app/main/default/objects/vf_TrainingResource__c

# Fourth batch - Objects that depend on third batch
sf project deploy start --source-dir force-app/main/default/objects/vf_Activity__c
sf project deploy start --source-dir force-app/main/default/objects/vf_Feedback__c
sf project deploy start --source-dir force-app/main/default/objects/vf_OnboardingChecklist__c
sf project deploy start --source-dir force-app/main/default/objects/vf_Recognition__c
sf project deploy start --source-dir force-app/main/default/objects/vf_BurnoutAssessment__c
sf project deploy start --source-dir force-app/main/default/objects/vf_ReengagementRecommendation__c
sf project deploy start --source-dir force-app/main/default/objects/vf_Notification__c
```

## Component-Specific Deployment

### Deploy Service Components

1. Deploy OnboardingPro components:
```bash
sf project deploy start --source-files \
    force-app/main/default/classes/OnboardingProService.cls \
    force-app/main/default/classes/OnboardingProAction.cls \
    force-app/main/default/flows/OnboardingProFlow.flow-meta.xml
```

2. Deploy RetentionGuard components:
```bash
sf project deploy start --source-files \
    force-app/main/default/classes/RetentionGuardService.cls \
    force-app/main/default/classes/RetentionGuardAction.cls \
    force-app/main/default/flows/RetentionGuardFlow.flow-meta.xml
```

3. Deploy MatchMaker components:
```bash
sf project deploy start --source-files \
    force-app/main/default/classes/MatchMakerService.cls \
    force-app/main/default/classes/MatchMakerAction.cls \
    force-app/main/default/flows/MatchMakerFlow.flow-meta.xml
```

## Validation

1. Validate deployment without actually deploying:
```bash
sf project deploy start --source-dir force-app --dry-run
```

2. Run Apex tests:
```bash
sf apex test run --test-level RunLocalTests --wait 10
```

## Retrieving Components

If you need to pull changes from the org:

1. Retrieve all components:
```bash
sf project retrieve start --source-dir force-app
```

2. Retrieve specific components:
```bash
sf project retrieve start --source-files \
    force-app/main/default/classes/OnboardingProService.cls \
    force-app/main/default/flows/OnboardingProFlow.flow-meta.xml
```

## Development Best Practices

1. Create a scratch org for development:
```bash
sf org create scratch --definition-file config/project-scratch-def.json --alias volunteerforce-dev
```

2. Push changes to scratch org:
```bash
sf project deploy start --source-dir force-app --target-org volunteerforce-dev
```

3. Pull changes from scratch org:
```bash
sf project retrieve start --source-dir force-app --target-org volunteerforce-dev
```

## Troubleshooting

1. Clear local cache:
```bash
sf cache clear
```

2. Check org limits:
```bash
sf limits api display
```

3. View deployment errors:
```bash
sf project deploy report --json
```

4. Check org status:
```bash
sf org display
```

## Additional Resources

- [Salesforce CLI Command Reference](https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/)
- [Salesforce DX Developer Guide](https://developer.salesforce.com/docs/atlas.en-us.sfdx_dev.meta/sfdx_dev/)
- [Visual Studio Code Extension Pack for Salesforce](https://marketplace.visualstudio.com/items?itemName=salesforce.salesforcedx-vscode)

## Notes

1. Always backup your org before deploying changes
2. Test deployments in a sandbox first
3. Follow your organization's deployment process
4. Keep track of dependencies between components
5. Use version control (e.g., Git) to manage your source code 