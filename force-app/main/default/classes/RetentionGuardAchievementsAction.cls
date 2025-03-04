public class RetentionGuardAchievementsAction {
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
}