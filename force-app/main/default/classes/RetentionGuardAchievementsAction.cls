public class RetentionGuardAchievementsAction {
    // Debug flag to return demo data instead of calling service
    public static Boolean DEBUG = true;
    
    @InvocableMethod(label='Identify Achievements' 
                     description='Identifies volunteer achievements eligible for recognition'
                     category='AgentForce - RetentionGuard')
    public static List<JsonResult> identifyAchievements(List<String> volunteerIds) {
        List<JsonResult> results = new List<JsonResult>();
        
        if (DEBUG) {
            // Return demo data for each request
            for (Integer i = 0; i < volunteerIds.size(); i++) {
                JsonResult result = new JsonResult();
                result.jsonResponse = getDemoAchievementsResponse();
                results.add(result);
            }
            return results;
        }
        
        // Original implementation
        for (String volunteerId : volunteerIds) {
            RetentionGuardService.AchievementsResponse response = RetentionGuardService.identifyAchievements(volunteerId);
            
            JsonResult result = new JsonResult();
            result.jsonResponse = JSON.serialize(response);
            results.add(result);
        }
        
        return results;
    }
    
    private static String getDemoAchievementsResponse() {
        return '{"volunteerId":"a0N8Z000000KoUYUA0","volunteerName":"Sarah Williams","recentAchievements":[{"id":"a0P8Z000000LpUYUA0","name":"100 Hours Milestone","description":"Completed 100 hours of service","date":"2024-02-15","type":"Service Hours","value":100},{"id":"a0P8Z000000LpUZUA0","name":"Project Leadership","description":"Successfully led the community garden project","date":"2024-01-30","type":"Leadership","value":null}],"upcomingMilestones":[{"name":"6 Month Anniversary","description":"Six months of continuous service","targetDate":"2024-04-10","type":"Tenure","currentValue":5,"targetValue":6,"progressPercentage":83},{"name":"Skills Certification","description":"Complete all required training modules","targetDate":"2024-05-15","type":"Certification","currentValue":4,"targetValue":5,"progressPercentage":80}],"recommendedRecognitions":[{"type":"Digital Badge","name":"Dedicated Volunteer","description":"For consistent participation and reliability"},{"type":"Certificate","name":"Project Leadership","description":"For taking initiative in leading volunteer activities"},{"type":"Public Recognition","name":"Volunteer Spotlight","description":"Feature in the monthly newsletter"}]}';
    }
    
    public class JsonResult {
        @InvocableVariable(required=true)
        public String jsonResponse;
    }
}