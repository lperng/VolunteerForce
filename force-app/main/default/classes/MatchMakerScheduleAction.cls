public class MatchMakerScheduleAction {
    // Debug flag to return demo data instead of calling service
    public static Boolean DEBUG = true;
    
    @InvocableMethod(label='Schedule Assignment' 
                     description='Schedules a volunteer for a project'
                     category='AgentForce - MatchMaker')
    public static List<JsonResult> scheduleAssignment(List<ScheduleRequest> requests) {
        List<JsonResult> results = new List<JsonResult>();
        
        if (DEBUG) {
            // Return demo data for each request
            for (Integer i = 0; i < requests.size(); i++) {
                JsonResult result = new JsonResult();
                result.jsonResponse = getDemoScheduleResponse(requests[i].volunteerId, requests[i].projectId);
                results.add(result);
            }
            return results;
        }
        
        // Original implementation
        for (ScheduleRequest request : requests) {
            MatchMakerService.ScheduleResponse response = MatchMakerService.scheduleAssignment(request.volunteerId, request.projectId);
            
            JsonResult result = new JsonResult();
            result.jsonResponse = JSON.serialize(response);
            results.add(result);
        }
        
        return results;
    }
    
    private static String getDemoScheduleResponse(String volunteerId, String projectId) {
        return '{"success":true,"assignmentId":"a0S8Z000000OsUYUA0","volunteerId":"' + volunteerId + '","volunteerName":"David Thompson","projectId":"' + projectId + '","projectName":"Community Garden Renovation","startDate":"2024-04-15","endDate":"2024-06-30","status":"Scheduled","message":"Successfully scheduled David Thompson for the Community Garden Renovation project","nextSteps":["Complete orientation on April 10th","Review project materials sent via email","Connect with project coordinator"],"orientation":{"date":"2024-04-10","time":"6:00 PM","location":"Community Center, Room 101","contactPerson":"Maria Garcia","contactEmail":"maria@example.org"}}';
    }
    
    public class ScheduleRequest {
        @InvocableVariable(required=true label='Volunteer ID' description='ID of the volunteer')
        public String volunteerId;
        
        @InvocableVariable(required=true label='Project ID' description='ID of the project')
        public String projectId;
    }
    
    public class JsonResult {
        @InvocableVariable(required=true)
        public String jsonResponse;
    }
}