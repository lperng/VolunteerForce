public class RetentionGuardService {
    private static final String BASE_URL = 'http://localhost:8000'; // Replace with actual server URL
    
    public class BurnoutRiskResponse {
        @AuraEnabled public String volunteerId { get; set; }
        @AuraEnabled public String volunteerName { get; set; }
        @AuraEnabled public String assessmentDate { get; set; }
        @AuraEnabled public Decimal riskProbability { get; set; }
        @AuraEnabled public String riskLevel { get; set; }
        @AuraEnabled public List<String> riskFactors { get; set; }
        @AuraEnabled public EngagementMetrics engagementMetrics { get; set; }
        @AuraEnabled public List<String> recommendedStrategies { get; set; }
    }
    
    public class EngagementMetrics {
        @AuraEnabled public Decimal activityFrequency { get; set; }
        @AuraEnabled public Integer daysSinceLastActivity { get; set; }
        @AuraEnabled public Decimal weeklyHours { get; set; }
        @AuraEnabled public Decimal satisfactionTrend { get; set; }
    }
    
    public class Achievement {
        @AuraEnabled public String type { get; set; }
        @AuraEnabled public String description { get; set; }
        @AuraEnabled public String dateAchieved { get; set; }
        @AuraEnabled public Map<String, Object> metrics { get; set; }
    }
    
    public class AchievementsResponse {
        @AuraEnabled public String volunteerId { get; set; }
        @AuraEnabled public List<Achievement> achievements { get; set; }
    }
    
    public class ReengagementStrategy {
        @AuraEnabled public String type { get; set; }
        @AuraEnabled public String description { get; set; }
        @AuraEnabled public String priority { get; set; }
        @AuraEnabled public List<String> actionItems { get; set; }
    }
    
    public class ReengagementResponse {
        @AuraEnabled public String volunteerId { get; set; }
        @AuraEnabled public List<ReengagementStrategy> strategies { get; set; }
    }
    
    @InvocableMethod(label='Predict Burnout Risk' 
                     description='Assesses the burnout risk for a specific volunteer')
    public static List<BurnoutRiskResponse> predictBurnoutRisk(List<String> volunteerIds) {
        List<BurnoutRiskResponse> responses = new List<BurnoutRiskResponse>();
        
        for (String volunteerId : volunteerIds) {
            Http http = new Http();
            HttpRequest req = new HttpRequest();
            req.setEndpoint(BASE_URL + '/retention/burnout-risk/' + volunteerId);
            req.setMethod('GET');
            
            try {
                HttpResponse res = http.send(req);
                if (res.getStatusCode() == 200) {
                    responses.add((BurnoutRiskResponse)JSON.deserialize(res.getBody(), BurnoutRiskResponse.class));
                } else {
                    throw new VolunteerForceException('Error predicting burnout risk: ' + res.getBody());
                }
            } catch (Exception e) {
                throw new VolunteerForceException('Error calling RetentionGuard API: ' + e.getMessage());
            }
        }
        
        return responses;
    }
    
    @AuraEnabled(cacheable=true)
    public static AchievementsResponse identifyAchievements(String volunteerId) {
        Http http = new Http();
        HttpRequest req = new HttpRequest();
        req.setEndpoint(BASE_URL + '/retention/achievements/' + volunteerId);
        req.setMethod('GET');
        
        try {
            HttpResponse res = http.send(req);
            if (res.getStatusCode() == 200) {
                return (AchievementsResponse)JSON.deserialize(res.getBody(), AchievementsResponse.class);
            } else {
                throw new VolunteerForceException('Error identifying achievements: ' + res.getBody());
            }
        } catch (Exception e) {
            throw new VolunteerForceException('Error calling RetentionGuard API: ' + e.getMessage());
        }
    }
    
    @AuraEnabled
    public static ReengagementResponse suggestReengagementStrategies(String volunteerId, String riskLevel) {
        Http http = new Http();
        HttpRequest req = new HttpRequest();
        req.setEndpoint(BASE_URL + '/retention/reengagement');
        req.setMethod('POST');
        req.setHeader('Content-Type', 'application/json');
        
        // Prepare request body
        Map<String, String> requestBody = new Map<String, String>{
            'volunteer_id' => volunteerId
        };
        if (String.isNotBlank(riskLevel)) {
            requestBody.put('risk_level', riskLevel);
        }
        req.setBody(JSON.serialize(requestBody));
        
        try {
            HttpResponse res = http.send(req);
            if (res.getStatusCode() == 200) {
                return (ReengagementResponse)JSON.deserialize(res.getBody(), ReengagementResponse.class);
            } else {
                throw new VolunteerForceException('Error suggesting reengagement strategies: ' + res.getBody());
            }
        } catch (Exception e) {
            throw new VolunteerForceException('Error calling RetentionGuard API: ' + e.getMessage());
        }
    }
    
    public class VolunteerForceException extends Exception {}
} 