public class MatchMakerFindAction {
    // Debug flag to return demo data instead of calling service
    public static Boolean DEBUG = true;
    
    @InvocableMethod(label='Find Project Matches' 
                     description='Finds best matching projects for a specific volunteer'
                     category='AgentForce - MatchMaker')
    public static List<JsonResult> findMatches(List<MatchMakerService.FindMatchesRequest> requests) {
        List<JsonResult> results = new List<JsonResult>();
        
        if (DEBUG) {
            // Return demo data for each request
            for (Integer i = 0; i < requests.size(); i++) {
                JsonResult result = new JsonResult();
                result.jsonResponse = getDemoProjectMatchesResult();
                results.add(result);
            }
            return results;
        }
        
        // Original implementation
        List<MatchMakerService.ProjectMatchesResult> responses = MatchMakerService.findMatches(requests);
        
        for (MatchMakerService.ProjectMatchesResult response : responses) {
            JsonResult result = new JsonResult();
            result.jsonResponse = JSON.serialize(response);
            results.add(result);
        }
        
        return results;
    }
    
    private static String getDemoProjectMatchesResult() {
        return '{"volunteerId":"a0N8Z000000KoUYUA0","volunteerName":"Emily Rodriguez","totalMatches":3,"matches":[{"projectId":"a0Q8Z000000MqUYUA0","projectName":"Community Garden Renovation","matchScore":92,"skillMatch":{"matched":["Gardening","Landscaping","Community Organizing"],"missing":["Heavy Lifting"]},"locationDistance":3.2,"availabilityMatch":{"matchPercentage":85,"conflictDays":["Wednesday evenings"]},"startDate":"2024-04-15","endDate":"2024-06-30","roles":[{"roleId":"a0R8Z000000NrUYUA0","roleName":"Garden Coordinator","required":["Leadership","Communication"],"recommended":["Gardening Experience"]}]},{"projectId":"a0Q8Z000000MqUZUA0","projectName":"Youth Mentorship Program","matchScore":85,"skillMatch":{"matched":["Communication","Leadership","Youth Work"],"missing":["Counseling Certification"]},"locationDistance":5.7,"availabilityMatch":{"matchPercentage":75,"conflictDays":["Monday mornings"]},"startDate":"2024-05-01","endDate":"2024-08-31","roles":[{"roleId":"a0R8Z000000NrUZUA0","roleName":"Youth Mentor","required":["Communication"],"recommended":["Teaching Experience","Patience"]}]},{"projectId":"a0Q8Z000000MqUaUA0","projectName":"Food Bank Distribution","matchScore":78,"skillMatch":{"matched":["Organization","Communication","Physical Stamina"],"missing":[]},"locationDistance":7.3,"availabilityMatch":{"matchPercentage":60,"conflictDays":["Saturday mornings","Tuesday evenings"]},"startDate":"2024-04-01","endDate":"2024-12-31","roles":[{"roleId":"a0R8Z000000NrUaUA0","roleName":"Distribution Assistant","required":["Organization"],"recommended":["Logistics Experience"]}]}],"recommendedProject":{"projectId":"a0Q8Z000000MqUYUA0","projectName":"Community Garden Renovation","matchScore":92,"reasonForRecommendation":"High skill match and close to your location"}}';
    }
    
    public class JsonResult {
        @InvocableVariable(required=true)
        public String jsonResponse;
    }
}