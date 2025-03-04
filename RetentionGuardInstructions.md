# AgentForce Implementation Guide

## RetentionGuard Agent Configuration

### Overview
The RetentionGuard agent proactively monitors volunteer engagement patterns, identifies potential burnout, recognizes achievements, and suggests personalized retention strategies. This document outlines the agent's configuration and implementation details.

### Topic Configuration

#### Basic Information
- **Developer Name**: RetentionGuard
- **Master Label**: RetentionGuard
- **Description**: Monitors engagement, identifies burnout risks, recognizes achievements, and suggests re-engagement strategies

#### Classification & Scope
- **Classification Description**: This topic addresses volunteer retention by monitoring engagement patterns, identifying early warning signs of burnout, recognizing volunteer achievements, and providing personalized re-engagement strategies.
- **Scope**: The agent's job is to analyze volunteer activities and feedback to predict burnout risk, identify achievements eligible for recognition, and suggest appropriate retention interventions based on risk level.

### Instructions for Agent
1. When assessing burnout risk:
   - Use 'Predict Burnout Risk' action
   - Provide volunteer ID
   - Review risk level, factors, and recommended strategies
   - Alert managers for high-risk volunteers

2. For achievement recognition:
   - Use 'Identify Achievements' action
   - Provide volunteer ID
   - Review eligible achievements
   - Trigger recognition notifications

3. When suggesting re-engagement strategies:
   - Use 'Suggest Reengagement Strategies' action
   - Provide volunteer ID and optional risk level
   - Present strategies based on risk level
   - Implement strategies through appropriate channels

### Agent Actions

#### 1. Predict Burnout Risk
```xml
<agentAction>
    <developerName>Predict_Burnout_Risk</developerName>
    <masterLabel>Predict Burnout Risk</masterLabel>
    <description>Assesses the burnout risk for a specific volunteer</description>
    <inputs>
        <volunteerId type="String" required="true"/>
    </inputs>
    <outputs>
        <burnoutRiskResponse type="BurnoutRiskResponse">
            <volunteerId type="String"/>
            <volunteerName type="String"/>
            <assessmentDate type="String"/>
            <riskProbability type="Decimal"/>
            <riskLevel type="String"/>
            <riskFactors type="String[]"/>
            <engagementMetrics type="EngagementMetrics">
                <activityFrequency type="Decimal"/>
                <daysSinceLastActivity type="Integer"/>
                <weeklyHours type="Decimal"/>
                <satisfactionTrend type="Decimal"/>
            </engagementMetrics>
            <recommendedStrategies type="String[]"/>
        </burnoutRiskResponse>
    </outputs>
</agentAction>
```

#### 2. Identify Achievements
```xml
<agentAction>
    <developerName>Identify_Achievements</developerName>
    <masterLabel>Identify Achievements</masterLabel>
    <description>Identifies volunteer achievements eligible for recognition</description>
    <inputs>
        <volunteerId type="String" required="true"/>
    </inputs>
    <outputs>
        <achievementsResponse type="AchievementsResponse">
            <volunteerId type="String"/>
            <achievements type="Achievement[]">
                <type type="String"/>
                <value type="String"/>
                <name type="String"/>
                <description type="String"/>
            </achievements>
        </achievementsResponse>
    </outputs>
</agentAction>
```

#### 3. Suggest Reengagement Strategies
```xml
<agentAction>
    <developerName>Suggest_Reengagement_Strategies</developerName>
    <masterLabel>Suggest Reengagement Strategies</masterLabel>
    <description>Suggests personalized reengagement strategies for a volunteer</description>
    <inputs>
        <volunteerId type="String" required="true" label="Volunteer ID" description="ID of the volunteer"/>
        <riskLevel type="String" required="false" label="Risk Level" description="Optional risk level for targeted strategies"/>
    </inputs>
    <outputs>
        <reengagementResponse type="ReengagementResponse">
            <volunteerId type="String"/>
            <strategies type="ReengagementStrategy[]">
                <type type="String"/>
                <description type="String"/>
                <priority type="String"/>
                <actionItems type="String[]"/>
            </strategies>
        </reengagementResponse>
    </outputs>
</agentAction>
```

#### 4. Trigger Recognition
```xml
<agentAction>
    <developerName>Trigger_Recognition</developerName>
    <masterLabel>Trigger Recognition</masterLabel>
    <description>Triggers a recognition event for a volunteer achievement</description>
    <inputs>
        <volunteerId type="String" required="true"/>
        <achievementType type="String" required="false"/>
        <achievementValue type="String" required="false"/>
    </inputs>
    <outputs>
        <recognitionId type="String"/>
        <volunteerName type="String"/>
        <achievement type="Achievement"/>
        <status type="String"/>
    </outputs>
</agentAction>
```

#### 5. Track Engagement Metrics
```xml
<agentAction>
    <developerName>Track_Engagement_Metrics</developerName>
    <masterLabel>Track Engagement Metrics</masterLabel>
    <description>Tracks key engagement metrics for a volunteer over time</description>
    <inputs>
        <volunteerId type="String" required="true"/>
        <daysBack type="Integer" required="false" default="90"/>
    </inputs>
    <outputs>
        <activityFrequency type="Decimal"/>
        <daysSinceLastActivity type="Integer"/>
        <weeklyHours type="Decimal"/>
        <hoursVolatility type="Decimal"/>
        <feedbackSentiment type="Decimal"/>
        <satisfactionTrend type="Decimal"/>
    </outputs>
</agentAction>
```

### Implementation Notes

1. **Data Types**
   - `BurnoutRiskResponse`: Burnout risk assessment with factors and metrics
   - `EngagementMetrics`: Key metrics about volunteer engagement
   - `Achievement`: Volunteer achievement with metadata
   - `ReengagementStrategy`: Suggested strategy with action items
   - `AchievementsResponse`: Collection of achievements for recognition

2. **Burnout Risk Assessment**
   - Uses ML model trained on historical data
   - Considers activity frequency and patterns
   - Analyzes feedback sentiment and trends
   - Evaluates workload and schedule consistency

3. **Achievement Recognition**
   - Identifies milestones (hours, projects, tenure)
   - Recognizes skill development 
   - Tracks certification accomplishments
   - Delivers personalized recognition

4. **Reengagement Strategies**
   - Tailored to risk level and volunteer profile
   - Range from appreciation to direct intervention
   - Include specific action items for coordinators
   - Track effectiveness of interventions

### Best Practices

1. **Risk Monitoring**
   - Assess all volunteers regularly
   - Prioritize high-risk cases
   - Monitor intervention effectiveness
   - Track organizational trends

2. **Recognition Program**
   - Acknowledge achievements promptly
   - Personalize recognition approach
   - Involve project managers and peers
   - Scale recognition to achievement significance

3. **Intervention Timing**
   - Intervene early for best results
   - Gradually escalate approaches
   - Involve direct supervisors
   - Document intervention outcomes

4. **Data Privacy**
   - Handle engagement data sensitively
   - Limit access to risk assessments
   - Follow organizational policies
   - Maintain volunteer confidentiality