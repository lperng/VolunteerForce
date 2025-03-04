public class OnboardingProResourcesAction {
    // Debug flag to return demo data instead of calling service
    public static Boolean DEBUG = true;
    
    @InvocableMethod(label='Recommend Learning Resources' 
                     description='Recommends additional learning resources for a specific module'
                     category='AgentForce - OnboardingPro')
    public static List<JsonResult> recommendResources(List<ResourceRequest> requests) {
        List<JsonResult> results = new List<JsonResult>();
        
        if (DEBUG) {
            // Return demo data for each request
            for (Integer i = 0; i < requests.size(); i++) {
                JsonResult result = new JsonResult();
                result.jsonResponse = getDemoResourcesResponse();
                results.add(result);
            }
            return results;
        }
        
        // Original implementation
        for (ResourceRequest request : requests) {
            List<OnboardingProService.ResourceResponse> resources = OnboardingProService.recommendResources(request.volunteerId, request.moduleId);
            
            JsonResult result = new JsonResult();
            result.jsonResponse = JSON.serialize(resources);
            results.add(result);
        }
        
        return results;
    }
    
    private static String getDemoResourcesResponse() {
        return '[{"id":"a0L8Z000000ImUYUA0","name":"Volunteer Management Guide","type":"PDF","url":"https://example.com/resources/vm_guide.pdf","learningStyle":"Reading","description":"Comprehensive guide to volunteer management principles"},{"id":"a0L8Z000000ImUZUA0","name":"Team Leadership Video Series","type":"Video","url":"https://example.com/videos/leadership","learningStyle":"Visual","description":"Video series on effective leadership techniques"},{"id":"a0L8Z000000ImUaUA0","name":"Interactive Communication Workshop","type":"Interactive","url":"https://example.com/workshops/communication","learningStyle":"Hands-on","description":"Practice communication skills with interactive exercises"}]';
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