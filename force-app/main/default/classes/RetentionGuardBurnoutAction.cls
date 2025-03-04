public class RetentionGuardBurnoutAction {
    @InvocableMethod(label='Predict Burnout Risk' 
                     description='Assesses the burnout risk for a specific volunteer'
                     category='AgentForce - RetentionGuard')
    public static List<BurnoutRiskResult> predictBurnoutRisk(List<String> volunteerIds) {
        List<RetentionGuardService.BurnoutRiskResponse> responses = RetentionGuardService.predictBurnoutRisk(volunteerIds);
        List<BurnoutRiskResult> results = new List<BurnoutRiskResult>();
        
        for (RetentionGuardService.BurnoutRiskResponse response : responses) {
            BurnoutRiskResult result = new BurnoutRiskResult();
            result.burnoutRiskResponse = response;
            results.add(result);
        }
        
        return results;
    }
    
    public class BurnoutRiskResult {
        @InvocableVariable(required=true)
        public RetentionGuardService.BurnoutRiskResponse burnoutRiskResponse;
    }
}