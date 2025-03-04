public class MatchMakerScheduleAction {
    @InvocableMethod(label='Schedule Assignment' 
                     description='Schedules a volunteer for a project'
                     category='AgentForce - MatchMaker')
    public static List<JsonResult> scheduleAssignment(List<ScheduleRequest> requests) {
        List<JsonResult> results = new List<JsonResult>();
        
        for (ScheduleRequest request : requests) {
            MatchMakerService.ScheduleResponse response = MatchMakerService.scheduleAssignment(request.volunteerId, request.projectId);
            
            JsonResult result = new JsonResult();
            result.jsonResponse = JSON.serialize(response);
            results.add(result);
        }
        
        return results;
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