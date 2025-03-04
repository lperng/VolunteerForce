# AgentForce Implementation Guide

## MatchMaker Agent Configuration

### Overview
The MatchMaker agent is designed to optimize volunteer-project matching by analyzing skills, availability, and preferences to create successful pairings. This document outlines the agent's configuration and implementation details.

### Topic Configuration

#### Basic Information
- **Developer Name**: MatchMaker
- **Master Label**: MatchMaker
- **Description**: Matches volunteers with projects based on skills, availability, and preferences

#### Classification & Scope
- **Classification Description**: This topic addresses matching volunteers with appropriate projects based on their skills, availability, and preferences, ensuring optimal project assignments and scheduling.
- **Scope**: The agent's job is to analyze volunteer profiles and project requirements to create optimal matches using machine learning and natural language processing, while managing the scheduling and notification process for successful matches.

### Instructions for Agent
1. When finding matches for a volunteer:
   - Use 'Find Project Matches' action
   - Provide volunteer ID as input
   - Review returned list of recommended projects with match scores

2. Profile Validation:
   - Check if volunteer profile is complete
   - Gather skills and availability information if incomplete
   - Use 'Get Volunteer Profile' action to retrieve data

3. Assignment Scheduling:
   - Use 'Schedule Assignment' action
   - Require both volunteer ID and project ID
   - Verify match score exceeds 0.65 threshold
   - Send notifications to all parties

### Agent Actions

#### 1. Find Project Matches
```xml
<agentAction>
    <developerName>Find_Project_Matches</developerName>
    <masterLabel>Find Project Matches</masterLabel>
    <description>Finds best matching projects for a specific volunteer</description>
    <inputs>
        <volunteerId type="String" required="true"/>
        <topN type="Integer" required="false" default="5"/>
    </inputs>
    <outputs>
        <matches type="ProjectMatch[]"/>
    </outputs>
</agentAction>
```

#### 2. Get Volunteer Profile
```xml
<agentAction>
    <developerName>Get_Volunteer_Profile</developerName>
    <masterLabel>Get Volunteer Profile</masterLabel>
    <description>Retrieves volunteer profile with skills and availability</description>
    <inputs>
        <volunteerId type="String" required="true"/>
    </inputs>
    <outputs>
        <profile type="VolunteerProfile"/>
    </outputs>
</agentAction>
```

#### 3. Schedule Assignment
```xml
<agentAction>
    <developerName>Schedule_Assignment</developerName>
    <masterLabel>Schedule Assignment</masterLabel>
    <description>Schedules a volunteer for a project and sends notifications</description>
    <inputs>
        <volunteerId type="String" required="true"/>
        <projectId type="String" required="true"/>
    </inputs>
    <outputs>
        <assignmentId type="String"/>
        <success type="Boolean"/>
    </outputs>
</agentAction>
```

#### 4. Send Assignment Notifications
```xml
<agentAction>
    <developerName>Send_Assignment_Notifications</developerName>
    <masterLabel>Send Assignment Notifications</masterLabel>
    <description>Sends notifications about new assignments to volunteers and project managers</description>
    <inputs>
        <assignmentId type="String" required="true"/>
    </inputs>
    <outputs>
        <success type="Boolean"/>
    </outputs>
</agentAction>
```

#### 5. Get Project Details
```xml
<agentAction>
    <developerName>Get_Project_Details</developerName>
    <masterLabel>Get Project Details</masterLabel>
    <description>Retrieves project details including requirements and schedule</description>
    <inputs>
        <projectId type="String" required="true"/>
    </inputs>
    <outputs>
        <project type="ProjectDetails"/>
    </outputs>
</agentAction>
```

### Implementation Notes

1. **Data Types**
   - `ProjectMatch[]`: Array of project matches with scores
   - `VolunteerProfile`: Volunteer details including skills and availability
   - `ProjectDetails`: Project information including requirements and schedule

2. **Matching Algorithm**
   - Uses ML for skill matching
   - Considers availability overlap
   - Factors in past performance
   - Applies location proximity scoring

3. **Notification System**
   - Automated notifications for assignments
   - Multi-channel delivery (email, SMS, in-app)
   - Configurable templates

4. **Security Considerations**
   - Validate user permissions
   - Secure data access
   - Audit logging for actions

### Best Practices

1. **Profile Management**
   - Always validate profile completeness
   - Update skills regularly
   - Keep availability current

2. **Match Quality**
   - Review match scores carefully
   - Consider both hard and soft skills
   - Factor in volunteer preferences

3. **Communication**
   - Send timely notifications
   - Include relevant details
   - Maintain audit trail

4. **Performance**
   - Monitor response times
   - Cache frequently accessed data
   - Optimize match calculations 