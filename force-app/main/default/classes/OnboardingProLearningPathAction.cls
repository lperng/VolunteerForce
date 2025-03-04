public class OnboardingProLearningPathAction {
    @InvocableMethod(label='Generate Learning Path' 
                     description='Generates a personalized learning path for a volunteer based on their role'
                     category='AgentForce - OnboardingPro')
    public static List<OnboardingProService.LearningPathResponse> generateLearningPath(List<OnboardingProRequest> requests) {
        List<OnboardingProService.GenerateLearningPathRequest> serviceRequests = new List<OnboardingProService.GenerateLearningPathRequest>();
        
        for (OnboardingProRequest request : requests) {
            OnboardingProService.GenerateLearningPathRequest serviceRequest = new OnboardingProService.GenerateLearningPathRequest();
            serviceRequest.volunteerId = request.volunteerId;
            serviceRequest.roleId = request.roleId;
            serviceRequests.add(serviceRequest);
        }
        
        return OnboardingProService.generateLearningPath(serviceRequests);
    }
    
    public class OnboardingProRequest {
        @InvocableVariable(required=true label='Volunteer ID' description='ID of the volunteer')
        public String volunteerId;
        
        @InvocableVariable(required=true label='Role ID' description='ID of the role')
        public String roleId;
    }
}