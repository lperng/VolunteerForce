public class MatchMakerScheduleAction {
    @InvocableMethod(label='Schedule Assignment' 
                     description='Schedules a volunteer for a project'
                     category='AgentForce - MatchMaker')
    public static List<ScheduleResponseResult> scheduleAssignment(List<ScheduleRequest> requests) {
        List<ScheduleResponseResult> responses = new List<ScheduleResponseResult>();
        
        for (ScheduleRequest request : requests) {
            ScheduleResponseResult result = new ScheduleResponseResult();
            result.response = MatchMakerService.scheduleAssignment(request.volunteerId, request.projectId);
            responses.add(result);
        }
        
        return responses;
    }
    
    public class ScheduleRequest {
        @InvocableVariable(required=true label='Volunteer ID' description='ID of the volunteer')
        public String volunteerId;
        
        @InvocableVariable(required=true label='Project ID' description='ID of the project')
        public String projectId;
    }
    
    public class ScheduleResponseResult {
        @InvocableVariable(required=true)
        public MatchMakerService.ScheduleResponse response;
    }
} 