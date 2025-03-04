public class RetentionGuardBurnoutAction {
    @InvocableMethod(label='Predict Burnout Risk' 
                     description='Assesses the burnout risk for a specific volunteer'
                     category='AgentForce - RetentionGuard')
    public static List<RetentionGuardService.BurnoutRiskResponse> predictBurnoutRisk(List<String> volunteerIds) {
        return RetentionGuardService.predictBurnoutRisk(volunteerIds);
    }
}