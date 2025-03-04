public class RetentionGuardAchievementsAction {
    @InvocableMethod(label='Identify Achievements' 
                     description='Identifies volunteer achievements eligible for recognition'
                     category='AgentForce - RetentionGuard')
    public static List<AchievementsResult> identifyAchievements(List<String> volunteerIds) {
        List<AchievementsResult> results = new List<AchievementsResult>();
        
        for (String volunteerId : volunteerIds) {
            AchievementsResult result = new AchievementsResult();
            result.achievementsResponse = RetentionGuardService.identifyAchievements(volunteerId);
            results.add(result);
        }
        
        return results;
    }
    
    public class AchievementsResult {
        @InvocableVariable(required=true)
        public RetentionGuardService.AchievementsResponse achievementsResponse;
    }
}