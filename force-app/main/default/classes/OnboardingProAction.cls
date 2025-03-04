public class OnboardingProAction {
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
    
    @InvocableMethod(label='Recommend Learning Resources' 
                     description='Recommends additional learning resources for a specific module'
                     category='AgentForce - OnboardingPro')
    public static List<List<OnboardingProService.ResourceResponse>> recommendResources(List<ResourceRequest> requests) {
        List<List<OnboardingProService.ResourceResponse>> responses = new List<List<OnboardingProService.ResourceResponse>>();
        
        for (ResourceRequest request : requests) {
            responses.add(OnboardingProService.recommendResources(request.volunteerId, request.moduleId));
        }
        
        return responses;
    }
    
    @InvocableMethod(label='Verify Certifications' 
                     description='Verifies volunteer certifications and identifies expiring ones'
                     category='AgentForce - OnboardingPro')
    public static List<OnboardingProService.CertificationResponse> verifyCertifications(List<String> volunteerIds) {
        List<OnboardingProService.CertificationResponse> responses = new List<OnboardingProService.CertificationResponse>();
        
        for (String volunteerId : volunteerIds) {
            responses.add(OnboardingProService.verifyCertifications(volunteerId));
        }
        
        return responses;
    }
    
    public class OnboardingProRequest {
        @InvocableVariable(required=true label='Volunteer ID' description='ID of the volunteer')
        public String volunteerId;
        
        @InvocableVariable(required=true label='Role ID' description='ID of the role')
        public String roleId;
    }
    
    public class ResourceRequest {
        @InvocableVariable(required=true label='Volunteer ID' description='ID of the volunteer')
        public String volunteerId;
        
        @InvocableVariable(required=true label='Module ID' description='ID of the training module')
        public String moduleId;
    }
} 