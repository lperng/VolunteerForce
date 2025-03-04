public class OnboardingProLearningPathAction {
    @InvocableMethod(label='Generate Learning Path' 
                     description='Generates a personalized learning path for a volunteer based on their role'
                     category='AgentForce - OnboardingPro')
    public static List<LearningPathResult> generateLearningPath(List<OnboardingProRequest> requests) {
        List<OnboardingProService.GenerateLearningPathRequest> serviceRequests = new List<OnboardingProService.GenerateLearningPathRequest>();
        List<LearningPathResult> results = new List<LearningPathResult>();
        
        for (OnboardingProRequest request : requests) {
            OnboardingProService.GenerateLearningPathRequest serviceRequest = new OnboardingProService.GenerateLearningPathRequest();
            serviceRequest.volunteerId = request.volunteerId;
            serviceRequest.roleId = request.roleId;
            serviceRequests.add(serviceRequest);
        }
        
        List<OnboardingProService.LearningPathResponse> responses = OnboardingProService.generateLearningPath(serviceRequests);
        
        // Convert service responses to invocable results
        for (OnboardingProService.LearningPathResponse response : responses) {
            LearningPathResult result = new LearningPathResult();
            result.learningPathResponse = response;
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
    
    public class LearningPathResult {
        @InvocableVariable(required=true)
        public OnboardingProService.LearningPathResponse learningPathResponse;
    }
}