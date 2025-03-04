public class MatchMakerFindAction {
    @InvocableMethod(label='Find Project Matches' 
                     description='Finds best matching projects for a specific volunteer'
                     category='AgentForce - MatchMaker')
    public static List<MatchMakerService.ProjectMatchesResult> findMatches(List<MatchMakerService.FindMatchesRequest> requests) {
        return MatchMakerService.findMatches(requests);
    }
} 