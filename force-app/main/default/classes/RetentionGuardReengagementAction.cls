public class RetentionGuardReengagementAction {
    // Debug flag to return demo data instead of calling service
    public static Boolean DEBUG = true;
    
    @InvocableMethod(label='Suggest Reengagement Strategies' 
                     description='Suggests personalized reengagement strategies for a volunteer'
                     category='AgentForce - RetentionGuard')
    public static List<JsonResult> suggestReengagementStrategies(List<ReengagementRequest> requests) {
        List<JsonResult> results = new List<JsonResult>();
        
        if (DEBUG) {
            // Return demo data for each request
            for (Integer i = 0; i < requests.size(); i++) {
                JsonResult result = new JsonResult();
                result.jsonResponse = getDemoReengagementResponse(requests[i].riskLevel);
                results.add(result);
            }
            return results;
        }
        
        // Original implementation
        for (ReengagementRequest request : requests) {
            RetentionGuardService.ReengagementResponse response = RetentionGuardService.suggestReengagementStrategies(request.volunteerId, request.riskLevel);
            
            JsonResult result = new JsonResult();
            result.jsonResponse = JSON.serialize(response);
            results.add(result);
        }
        
        return results;
    }
    
    private static String getDemoReengagementResponse(String riskLevel) {
        String defaultRiskLevel = 'Medium';
        if (riskLevel != null && riskLevel.trim() != '') {
            defaultRiskLevel = riskLevel;
        }
        
        return '{"volunteerId":"a0N8Z000000KoUYUA0","volunteerName":"Robert Chen","riskLevel":"' + defaultRiskLevel + '","creationDate":"2024-03-01","strategies":[{"category":"Communication","actions":["Schedule personal check-in call","Send personalized appreciation message","Invite to volunteer social event"],"priority":"High"},{"category":"Role Adjustment","actions":["Offer flexible scheduling options","Suggest alternative role based on interests","Reduce time commitment temporarily"],"priority":"Medium"},{"category":"Recognition","actions":["Present service certificate","Feature in volunteer spotlight","Nominate for volunteer award"],"priority":"Medium"},{"category":"Development","actions":["Offer skill-building workshop","Provide mentorship opportunity","Create leadership pathway"],"priority":"Low"}],"personalizedMessage":"Hi Robert, we\'ve noticed you\'ve been less active lately. We value your contributions and would love to chat about how we can make your volunteer experience more rewarding. Would you have time for a quick call this week?"}';
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