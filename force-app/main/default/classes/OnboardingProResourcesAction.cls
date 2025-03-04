public class OnboardingProResourcesAction {
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
    
    public class ResourceRequest {
        @InvocableVariable(required=true label='Volunteer ID' description='ID of the volunteer')
        public String volunteerId;
        
        @InvocableVariable(required=true label='Module ID' description='ID of the training module')
        public String moduleId;
    }
}