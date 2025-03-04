public class RetentionGuardReengagementAction {
    @InvocableMethod(label='Suggest Reengagement Strategies' 
                     description='Suggests personalized reengagement strategies for a volunteer'
                     category='AgentForce - RetentionGuard')
    public static List<JsonResult> suggestReengagementStrategies(List<ReengagementRequest> requests) {
        List<JsonResult> results = new List<JsonResult>();
        
        for (ReengagementRequest request : requests) {
            RetentionGuardService.ReengagementResponse response = RetentionGuardService.suggestReengagementStrategies(request.volunteerId, request.riskLevel);
            
            JsonResult result = new JsonResult();
            result.jsonResponse = JSON.serialize(response);
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
    
    public class JsonResult {
        @InvocableVariable(required=true)
        public String jsonResponse;
    }
}