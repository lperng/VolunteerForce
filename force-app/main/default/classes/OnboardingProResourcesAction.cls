public class OnboardingProResourcesAction {
    @InvocableMethod(label='Recommend Learning Resources' 
                     description='Recommends additional learning resources for a specific module'
                     category='AgentForce - OnboardingPro')
    public static List<JsonResult> recommendResources(List<ResourceRequest> requests) {
        List<JsonResult> results = new List<JsonResult>();
        
        for (ResourceRequest request : requests) {
            List<OnboardingProService.ResourceResponse> resources = OnboardingProService.recommendResources(request.volunteerId, request.moduleId);
            
            JsonResult result = new JsonResult();
            result.jsonResponse = JSON.serialize(resources);
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
    
    public class JsonResult {
        @InvocableVariable(required=true)
        public String jsonResponse;
    }
}