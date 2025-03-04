public class RetentionGuardReengagementAction {
    @InvocableMethod(label='Suggest Reengagement Strategies' 
                     description='Suggests personalized reengagement strategies for a volunteer'
                     category='AgentForce - RetentionGuard')
    public static List<ReengagementResult> suggestReengagementStrategies(List<ReengagementRequest> requests) {
        List<ReengagementResult> results = new List<ReengagementResult>();
        
        for (ReengagementRequest request : requests) {
            ReengagementResult result = new ReengagementResult();
            result.reengagementResponse = RetentionGuardService.suggestReengagementStrategies(request.volunteerId, request.riskLevel);
            results.add(result);
        }
        
        return results;
    }
    
    public class ReengagementRequest {
        @InvocableVariable(required=true label='Volunteer ID' description='ID of the volunteer')
        public String volunteerId;
        
        @InvocableVariable(required=false label='Risk Level' description='Optional risk level for targeted strategies')
        public String riskLevel;
    }
    
    public class ReengagementResult {
        @InvocableVariable(required=true)
        public RetentionGuardService.ReengagementResponse reengagementResponse;
    }
}