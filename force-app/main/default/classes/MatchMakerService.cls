public class MatchMakerService {
    private static final String BASE_URL = 'http://localhost:8000'; // Replace with actual server URL
    
    public class ProjectMatch {
        @AuraEnabled public String projectId { get; set; }
        @AuraEnabled public String projectName { get; set; }
        @AuraEnabled public Decimal overallScore { get; set; }
        @AuraEnabled public Decimal skillMatch { get; set; }
        @AuraEnabled public Decimal availabilityMatch { get; set; }
        @AuraEnabled public Decimal locationMatch { get; set; }
    }
    
    public class ProjectMatchesResult {
        @InvocableVariable(required=true)
        public List<ProjectMatch> matches;
    }
    
    public class MatchScores {
        @AuraEnabled public Decimal overallScore { get; set; }
        @AuraEnabled public Decimal skillMatch { get; set; }
        @AuraEnabled public Decimal availabilityMatch { get; set; }
        @AuraEnabled public Decimal locationMatch { get; set; }
    }
    
    public class ScheduleResponse {
        @AuraEnabled public Boolean success { get; set; }
        @AuraEnabled public String assignmentId { get; set; }
        @AuraEnabled public MatchScores matchScore { get; set; }
    }
    
    @InvocableMethod(label='Find Project Matches' 
                     description='Finds best matching projects for a specific volunteer')
    public static List<ProjectMatchesResult> findMatches(List<FindMatchesRequest> requests) {
        List<ProjectMatchesResult> responses = new List<ProjectMatchesResult>();
        
        for (FindMatchesRequest request : requests) {
            Http http = new Http();
            HttpRequest req = new HttpRequest();
            req.setEndpoint(BASE_URL + '/matchmaker/matches');
            req.setMethod('POST');
            req.setHeader('Content-Type', 'application/json');
            
            // Prepare request body
            Map<String, Object> requestBody = new Map<String, Object>{
                'volunteer_id' => request.volunteerId
            };
            if (request.topN != null) {
                requestBody.put('top_n', request.topN);
            }
            req.setBody(JSON.serialize(requestBody));
            
            try {
                HttpResponse res = http.send(req);
                if (res.getStatusCode() == 200) {
                    ProjectMatchesResult result = new ProjectMatchesResult();
                    result.matches = (List<ProjectMatch>)JSON.deserialize(res.getBody(), List<ProjectMatch>.class);
                    responses.add(result);
                } else {
                    throw new VolunteerForceException('Error finding matches: ' + res.getBody());
                }
            } catch (Exception e) {
                throw new VolunteerForceException('Error calling MatchMaker API: ' + e.getMessage());
            }
        }
        
        return responses;
    }
    
    @AuraEnabled
    public static ScheduleResponse scheduleAssignment(String volunteerId, String projectId) {
        Http http = new Http();
        HttpRequest req = new HttpRequest();
        req.setEndpoint(BASE_URL + '/matchmaker/schedule');
        req.setMethod('POST');
        req.setHeader('Content-Type', 'application/json');
        
        // Prepare request body
        Map<String, String> requestBody = new Map<String, String>{
            'volunteer_id' => volunteerId,
            'project_id' => projectId
        };
        req.setBody(JSON.serialize(requestBody));
        
        try {
            HttpResponse res = http.send(req);
            if (res.getStatusCode() == 200) {
                return (ScheduleResponse)JSON.deserialize(res.getBody(), ScheduleResponse.class);
            } else {
                throw new VolunteerForceException('Error scheduling assignment: ' + res.getBody());
            }
        } catch (Exception e) {
            throw new VolunteerForceException('Error calling MatchMaker API: ' + e.getMessage());
        }
    }
    
    public class FindMatchesRequest {
        @InvocableVariable(required=true label='Volunteer ID')
        public String volunteerId;
        
        @InvocableVariable(required=false label='Number of Top Matches')
        public Integer topN;
    }
    
    public class VolunteerForceException extends Exception {}
} 