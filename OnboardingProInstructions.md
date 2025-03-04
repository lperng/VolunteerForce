# AgentForce Implementation Guide

## OnboardingPro Agent Configuration

### Overview
The OnboardingPro agent creates personalized onboarding experiences for volunteers based on their skills, role requirements, and learning preferences. This document outlines the agent's configuration and implementation details.

### Topic Configuration

#### Basic Information
- **Developer Name**: OnboardingPro
- **Master Label**: OnboardingPro
- **Description**: Delivers personalized training paths, tracks certifications, and provides just-in-time learning resources

#### Classification & Scope
- **Classification Description**: This topic addresses volunteer onboarding and training by creating personalized learning paths, tracking certification requirements, and delivering targeted learning resources.
- **Scope**: The agent's job is to generate role-specific training paths, track progress through required training modules, recommend additional learning resources based on volunteer preferences, and verify certification status.

### Instructions for Agent
1. When creating a learning path:
   - Use 'Generate Learning Path' action
   - Provide both volunteer ID and role ID
   - Review returned learning path with required and recommended modules

2. For learning resource recommendations:
   - Use 'Recommend Learning Resources' action
   - Specify both volunteer ID and module ID
   - Present resources matching volunteer's learning preferences first

3. When verifying certifications:
   - Use 'Verify Certifications' action
   - Provide volunteer ID
   - Check for expired and soon-to-expire certifications
   - Trigger renewal notifications for expiring certifications

### Agent Actions

#### 1. Generate Learning Path
```xml
<agentAction>
    <developerName>Generate_Learning_Path</developerName>
    <masterLabel>Generate Learning Path</masterLabel>
    <description>Generates a personalized learning path for a volunteer based on their role</description>
    <inputs>
        <volunteerId type="String" required="true" label="Volunteer ID" description="ID of the volunteer"/>
        <roleId type="String" required="true" label="Role ID" description="ID of the role"/>
    </inputs>
    <outputs>
        <learningPathResponse type="LearningPathResponse">
            <volunteerId type="String"/>
            <roleId type="String"/>
            <totalModules type="Integer"/>
            <requiredModules type="Integer"/>
            <recommendedModules type="Integer"/>
            <estimatedHours type="Decimal"/>
            <modules type="LearningModule[]"/>
        </learningPathResponse>
    </outputs>
</agentAction>
```

#### 2. Recommend Learning Resources
```xml
<agentAction>
    <developerName>Recommend_Learning_Resources</developerName>
    <masterLabel>Recommend Learning Resources</masterLabel>
    <description>Recommends additional learning resources for a specific module</description>
    <inputs>
        <volunteerId type="String" required="true" label="Volunteer ID" description="ID of the volunteer"/>
        <moduleId type="String" required="true" label="Module ID" description="ID of the training module"/>
    </inputs>
    <outputs>
        <resources type="ResourceResponse[]">
            <resourceId type="String"/>
            <title type="String"/>
            <type type="String"/>
            <url type="String"/>
            <learningStyle type="String"/>
        </resources>
    </outputs>
</agentAction>
```

#### 3. Verify Certifications
```xml
<agentAction>
    <developerName>Verify_Certifications</developerName>
    <masterLabel>Verify Certifications</masterLabel>
    <description>Verifies volunteer certifications and identifies expiring ones</description>
    <inputs>
        <volunteerId type="String" required="true"/>
    </inputs>
    <outputs>
        <certificationResponse type="CertificationResponse">
            <volunteerId type="String"/>
            <validCertifications type="Integer"/>
            <expiringCertifications type="Integer"/>
            <expiredCertifications type="Integer"/>
            <certificationDetails type="CertificationDetails">
                <valid type="String[]"/>
                <expiring type="String[]"/>
                <expired type="String[]"/>
            </certificationDetails>
        </certificationResponse>
    </outputs>
</agentAction>
```

#### 4. Track Training Progress
```xml
<agentAction>
    <developerName>Track_Training_Progress</developerName>
    <masterLabel>Track Training Progress</masterLabel>
    <description>Tracks a volunteer's progress through their learning path</description>
    <inputs>
        <volunteerId type="String" required="true"/>
        <pathId type="String" required="false"/>
    </inputs>
    <outputs>
        <progressPercentage type="Decimal"/>
        <completedModules type="Integer"/>
        <totalModules type="Integer"/>
        <overdueModules type="Integer"/>
        <modules type="ModuleProgress[]"/>
    </outputs>
</agentAction>
```

#### 5. Create Onboarding Checklist
```xml
<agentAction>
    <developerName>Create_Onboarding_Checklist</developerName>
    <masterLabel>Create Onboarding Checklist</masterLabel>
    <description>Generates a personalized onboarding checklist for a volunteer-project assignment</description>
    <inputs>
        <volunteerId type="String" required="true"/>
        <projectId type="String" required="true"/>
    </inputs>
    <outputs>
        <checklistId type="String"/>
        <totalItems type="Integer"/>
        <completedItems type="Integer"/>
        <items type="ChecklistItem[]"/>
    </outputs>
</agentAction>
```

### Implementation Notes

1. **Data Types**
   - `LearningPathResponse`: Contains learning path details including modules
   - `LearningModule`: Individual training module with metadata
   - `ResourceResponse`: Learning resource with type and URL
   - `CertificationResponse`: Certification status summary
   - `ModuleProgress`: Training module completion status
   - `ChecklistItem`: Onboarding checklist item

2. **Learning Path Generation**
   - Analyzes role requirements and prerequisites
   - Considers volunteer's existing skills
   - Creates topologically sorted path (prerequisites first)
   - Estimates completion timeframes

3. **Learning Preferences**
   - Adapts to volunteer's learning style
   - Prioritizes visual, auditory, or kinesthetic resources
   - Personalizes resource recommendations

4. **Certification Tracking**
   - Validates certification expiration dates
   - Notifies of upcoming expirations
   - Recommends renewal procedures

### Best Practices

1. **Learning Path Management**
   - Generate new paths when roles change
   - Update for new skill requirements
   - Validate prerequisites are met

2. **Resource Recommendations**
   - Provide diverse learning formats
   - Match to volunteer's preferences
   - Ensure resources are current

3. **Certification Workflows**
   - Monitor expiration proactively
   - Schedule renewal reminders 
   - Verify completion of required certifications

4. **Onboarding Experience**
   - Create consistent, comprehensive checklists
   - Track completion progress
   - Automate follow-ups for incomplete items