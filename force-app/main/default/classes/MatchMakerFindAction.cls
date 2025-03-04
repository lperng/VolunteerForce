public class MatchMakerFindAction {
    @InvocableMethod(label='Find Project Matches' 
                     description='Finds best matching projects for a specific volunteer'
                     category='AgentForce - MatchMaker')
    public static List<JsonResult> findMatches(List<MatchMakerService.FindMatchesRequest> requests) {
        List<MatchMakerService.ProjectMatchesResult> responses = MatchMakerService.findMatches(requests);
        List<JsonResult> results = new List<JsonResult>();
        
        for (MatchMakerService.ProjectMatchesResult response : responses) {
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