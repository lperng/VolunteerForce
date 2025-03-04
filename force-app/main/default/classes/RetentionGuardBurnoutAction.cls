public class RetentionGuardBurnoutAction {
    // Debug flag to return demo data instead of calling service
    public static Boolean DEBUG = true;
    
    @InvocableMethod(label='Predict Burnout Risk' 
                     description='Assesses the burnout risk for a specific volunteer'
                     category='AgentForce - RetentionGuard')
    public static List<JsonResult> predictBurnoutRisk(List<String> volunteerIds) {
        List<JsonResult> results = new List<JsonResult>();
        
        if (DEBUG) {
            // Return demo data for each request
            for (Integer i = 0; i < volunteerIds.size(); i++) {
                JsonResult result = new JsonResult();
                result.jsonResponse = getDemoBurnoutRiskResponse();
                results.add(result);
            }
            return results;
        }
        
        // Original implementation
        List<RetentionGuardService.BurnoutRiskResponse> responses = RetentionGuardService.predictBurnoutRisk(volunteerIds);
        
        for (RetentionGuardService.BurnoutRiskResponse response : responses) {
            JsonResult result = new JsonResult();
            result.jsonResponse = JSON.serialize(response);
            results.add(result);
        }
        
        return results;
    }
    
    private static String getDemoBurnoutRiskResponse() {
        return '{"volunteerId":"a0N8Z000000KoUYUA0","volunteerName":"Michael Johnson","riskLevel":"Medium","riskProbability":0.45,"assessmentDate":"2024-03-01","riskFactors":["Decreased participation in team meetings","Increased no-shows for scheduled events","Reduced engagement in training activities"],"engagementMetrics":{"hoursPerMonth":[{"month":"January","hours":12},{"month":"February","hours":8}],"activitiesPerMonth":[{"month":"January","count":6},{"month":"February","count":3}],"feedbackTrend":"Declining"},"recommendedStrategies":["Schedule one-on-one check-in","Offer alternative volunteer roles","Provide recognition for past contributions","Consider temporary reduced schedule"]}';
    }
    
    public class JsonResult {
        @InvocableVariable(required=true)
        public String jsonResponse;
    }
}