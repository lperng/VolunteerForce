public class RetentionGuardBurnoutAction {
    @InvocableMethod(label='Predict Burnout Risk' 
                     description='Assesses the burnout risk for a specific volunteer'
                     category='AgentForce - RetentionGuard')
    public static List<JsonResult> predictBurnoutRisk(List<String> volunteerIds) {
        List<RetentionGuardService.BurnoutRiskResponse> responses = RetentionGuardService.predictBurnoutRisk(volunteerIds);
        List<JsonResult> results = new List<JsonResult>();
        
        for (RetentionGuardService.BurnoutRiskResponse response : responses) {
            JsonResult result = new JsonResult();
            result.jsonResponse = JSON.serialize(response);
            results.add(result);
        }
        
        return results;
    }
    
    public class JsonResult {
        @InvocableVariable(required=true)
        public String jsonResponse;
    }
}