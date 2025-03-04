public class RetentionGuardAction {
    @InvocableMethod(label='Predict Burnout Risk' 
                     description='Assesses the burnout risk for a specific volunteer'
                     category='AgentForce - RetentionGuard')
    public static List<RetentionGuardService.BurnoutRiskResponse> predictBurnoutRisk(List<String> volunteerIds) {
        return RetentionGuardService.predictBurnoutRisk(volunteerIds);
    }
    
    @InvocableMethod(label='Identify Achievements' 
                     description='Identifies volunteer achievements eligible for recognition'
                     category='AgentForce - RetentionGuard')
    public static List<RetentionGuardService.AchievementsResponse> identifyAchievements(List<String> volunteerIds) {
        List<RetentionGuardService.AchievementsResponse> responses = new List<RetentionGuardService.AchievementsResponse>();
        
        for (String volunteerId : volunteerIds) {
            responses.add(RetentionGuardService.identifyAchievements(volunteerId));
        }
        
        return responses;
    }
    
    @InvocableMethod(label='Suggest Reengagement Strategies' 
                     description='Suggests personalized reengagement strategies for a volunteer'
                     category='AgentForce - RetentionGuard')
    public static List<RetentionGuardService.ReengagementResponse> suggestReengagementStrategies(List<ReengagementRequest> requests) {
        List<RetentionGuardService.ReengagementResponse> responses = new List<RetentionGuardService.ReengagementResponse>();
        
        for (ReengagementRequest request : requests) {
            responses.add(RetentionGuardService.suggestReengagementStrategies(request.volunteerId, request.riskLevel));
        }
        
        return responses;
    }
    
    public class ReengagementRequest {
        @InvocableVariable(required=true label='Volunteer ID' description='ID of the volunteer')
        public String volunteerId;
        
        @InvocableVariable(required=false label='Risk Level' description='Optional risk level for targeted strategies')
        public String riskLevel;
    }
} 