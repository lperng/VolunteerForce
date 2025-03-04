public class OnboardingProResourcesAction {
    @InvocableMethod(label='Recommend Learning Resources' 
                     description='Recommends additional learning resources for a specific module'
                     category='AgentForce - OnboardingPro')
    public static List<ResourcesResult> recommendResources(List<ResourceRequest> requests) {
        List<ResourcesResult> results = new List<ResourcesResult>();
        
        for (ResourceRequest request : requests) {
            ResourcesResult result = new ResourcesResult();
            result.resources = OnboardingProService.recommendResources(request.volunteerId, request.moduleId);
            results.add(result);
        }
        
        return results;
    }
    
    public class ResourceRequest {
        @InvocableVariable(required=true label='Volunteer ID' description='ID of the volunteer')
        public String volunteerId;
        
        @InvocableVariable(required=true label='Module ID' description='ID of the training module')
        public String moduleId;
    }
    
    public class ResourcesResult {
        @InvocableVariable(required=true)
        public List<OnboardingProService.ResourceResponse> resources;
    }
}