public class RetentionGuardAchievementsAction {
    @InvocableMethod(label='Identify Achievements' 
                     description='Identifies volunteer achievements eligible for recognition'
                     category='AgentForce - RetentionGuard')
    public static List<JsonResult> identifyAchievements(List<String> volunteerIds) {
        List<JsonResult> results = new List<JsonResult>();
        
        for (String volunteerId : volunteerIds) {
            RetentionGuardService.AchievementsResponse response = RetentionGuardService.identifyAchievements(volunteerId);
            
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