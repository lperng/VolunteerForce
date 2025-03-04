public class RetentionGuardReengagementAction {
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