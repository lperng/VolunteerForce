public class OnboardingProLearningPathAction {
    // Debug flag to return demo data instead of calling service
    public static Boolean DEBUG = true;
    
    @InvocableMethod(label='Generate Learning Path' 
                     description='Generates a personalized learning path for a volunteer based on their role'
                     category='AgentForce - OnboardingPro')
    public static List<JsonResult> generateLearningPath(List<OnboardingProRequest> requests) {
        List<JsonResult> results = new List<JsonResult>();
        
        if (DEBUG) {
            // Return demo data for each request
            for (Integer i = 0; i < requests.size(); i++) {
                JsonResult result = new JsonResult();
                result.jsonResponse = getDemoLearningPathResponse();
                results.add(result);
            }
            return results;
        }
        
        // Original implementation
        List<OnboardingProService.GenerateLearningPathRequest> serviceRequests = new List<OnboardingProService.GenerateLearningPathRequest>();
        
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
    
    private static String getDemoLearningPathResponse() {
        return '{"learningPath":{"id":"a0J8Z000000GnUYUA0","volunteerName":"John Doe","role":"Project Coordinator","requiredModules":["Project Management Basics","Communication Skills","Team Leadership"],"optionalModules":["Risk Management","Budget Planning"],"progress":30,"estimatedCompletionTime":"10 hours"},"modules":[{"id":"a0K8Z000000HmTYUA0","name":"Project Management Basics","description":"Learn the fundamentals of project management","duration":120,"difficulty":"Beginner","completed":true},{"id":"a0K8Z000000HmTZUA0","name":"Communication Skills","description":"Effective communication techniques for volunteers","duration":90,"difficulty":"Beginner","completed":false},{"id":"a0K8Z000000HmTaUA0","name":"Team Leadership","description":"Leading volunteer teams effectively","duration":180,"difficulty":"Intermediate","completed":false},{"id":"a0K8Z000000HmTbUA0","name":"Risk Management","description":"Identifying and mitigating project risks","duration":120,"difficulty":"Advanced","completed":false},{"id":"a0K8Z000000HmTcUA0","name":"Budget Planning","description":"Basic budgeting for nonprofit projects","duration":90,"difficulty":"Intermediate","completed":false}]}';
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