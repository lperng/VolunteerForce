public class OnboardingProLearningPathAction {
    @InvocableMethod(label='Generate Learning Path' 
                     description='Generates a personalized learning path for a volunteer based on their role'
                     category='AgentForce - OnboardingPro')
    public static List<JsonResult> generateLearningPath(List<OnboardingProRequest> requests) {
        List<OnboardingProService.GenerateLearningPathRequest> serviceRequests = new List<OnboardingProService.GenerateLearningPathRequest>();
        List<JsonResult> results = new List<JsonResult>();
        
        for (OnboardingProRequest request : requests) {
            OnboardingProService.GenerateLearningPathRequest serviceRequest = new OnboardingProService.GenerateLearningPathRequest();
            serviceRequest.volunteerId = request.volunteerId;
            serviceRequest.roleId = request.roleId;
            serviceRequests.add(serviceRequest);
        }
        
        List<OnboardingProService.LearningPathResponse> responses = OnboardingProService.generateLearningPath(serviceRequests);
        
        // Convert service responses to JSON strings
        for (OnboardingProService.LearningPathResponse response : responses) {
            JsonResult result = new JsonResult();
            result.jsonResponse = JSON.serialize(response);
            results.add(result);
        }
        
        return results;
    }
    
    public class OnboardingProRequest {
        @InvocableVariable(required=true label='Volunteer ID' description='ID of the volunteer')
        public String volunteerId;
        
        @InvocableVariable(required=true label='Role ID' description='ID of the role')
        public String roleId;
    }
    
    public class JsonResult {
        @InvocableVariable(required=true)
        public String jsonResponse;
    }
}