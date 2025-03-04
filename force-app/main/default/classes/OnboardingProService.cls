public class OnboardingProService {
    private static final String BASE_URL = 'http://localhost:8000'; // Replace with actual server URL
    
    // Named Credentials can be used in production for secure endpoint configuration
    // private static final String NAMED_CREDENTIAL = 'VolunteerForce_API';
    
    public class LearningPathResponse {
        @AuraEnabled public String volunteerId { get; set; }
        @AuraEnabled public String roleId { get; set; }
        @AuraEnabled public List<LearningModule> learningPath { get; set; }
    }
    
    public class LearningModule {
        @AuraEnabled public String moduleId { get; set; }
        @AuraEnabled public String name { get; set; }
        @AuraEnabled public String description { get; set; }
        @AuraEnabled public Integer estimatedDuration { get; set; }
        @AuraEnabled public Integer priority { get; set; }
    }
    
    public class ResourceResponse {
        @AuraEnabled public String resourceId { get; set; }
        @AuraEnabled public String title { get; set; }
        @AuraEnabled public String type { get; set; }
        @AuraEnabled public String url { get; set; }
        @AuraEnabled public String learningStyle { get; set; }
    }
    
    public class CertificationResponse {
        @AuraEnabled public String volunteerId { get; set; }
        @AuraEnabled public Integer validCertifications { get; set; }
        @AuraEnabled public Integer expiringCertifications { get; set; }
        @AuraEnabled public Integer expiredCertifications { get; set; }
        @AuraEnabled public CertificationDetails certificationDetails { get; set; }
    }
    
    public class CertificationDetails {
        @AuraEnabled public List<String> valid { get; set; }
        @AuraEnabled public List<String> expiring { get; set; }
        @AuraEnabled public List<String> expired { get; set; }
    }
    
    public static List<LearningPathResponse> generateLearningPath(List<GenerateLearningPathRequest> requests) {
        List<LearningPathResponse> responses = new List<LearningPathResponse>();
        
        for (GenerateLearningPathRequest request : requests) {
            Http http = new Http();
            HttpRequest req = new HttpRequest();
            req.setEndpoint(BASE_URL + '/onboarding/learning-path');
            req.setMethod('POST');
            req.setHeader('Content-Type', 'application/json');
            
            // Prepare request body
            Map<String, String> requestBody = new Map<String, String>{
                'volunteer_id' => request.volunteerId,
                'role_id' => request.roleId
            };
            req.setBody(JSON.serialize(requestBody));
            
            try {
                HttpResponse res = http.send(req);
                if (res.getStatusCode() == 200) {
                    responses.add((LearningPathResponse)JSON.deserialize(res.getBody(), LearningPathResponse.class));
                } else {
                    throw new VolunteerForceException('Error generating learning path: ' + res.getBody());
                }
            } catch (Exception e) {
                throw new VolunteerForceException('Error calling OnboardingPro API: ' + e.getMessage());
            }
        }
        
        return responses;
    }
    
    @AuraEnabled(cacheable=true)
    public static List<ResourceResponse> recommendResources(String volunteerId, String moduleId) {
        Http http = new Http();
        HttpRequest req = new HttpRequest();
        req.setEndpoint(BASE_URL + '/onboarding/resources');
        req.setMethod('POST');
        req.setHeader('Content-Type', 'application/json');
        
        // Prepare request body
        Map<String, String> requestBody = new Map<String, String>{
            'volunteer_id' => volunteerId,
            'module_id' => moduleId
        };
        req.setBody(JSON.serialize(requestBody));
        
        try {
            HttpResponse res = http.send(req);
            if (res.getStatusCode() == 200) {
                return (List<ResourceResponse>)JSON.deserialize(res.getBody(), List<ResourceResponse>.class);
            } else {
                throw new VolunteerForceException('Error recommending resources: ' + res.getBody());
            }
        } catch (Exception e) {
            throw new VolunteerForceException('Error calling OnboardingPro API: ' + e.getMessage());
        }
    }
    
    @AuraEnabled(cacheable=true)
    public static CertificationResponse verifyCertifications(String volunteerId) {
        Http http = new Http();
        HttpRequest req = new HttpRequest();
        req.setEndpoint(BASE_URL + '/onboarding/certifications/' + volunteerId);
        req.setMethod('GET');
        
        try {
            HttpResponse res = http.send(req);
            if (res.getStatusCode() == 200) {
                return (CertificationResponse)JSON.deserialize(res.getBody(), CertificationResponse.class);
            } else {
                throw new VolunteerForceException('Error verifying certifications: ' + res.getBody());
            }
        } catch (Exception e) {
            throw new VolunteerForceException('Error calling OnboardingPro API: ' + e.getMessage());
        }
    }
    
    public class GenerateLearningPathRequest {
        @InvocableVariable(required=true label='Volunteer ID')
        public String volunteerId;
        
        @InvocableVariable(required=true label='Role ID')
        public String roleId;
    }
    
    public class VolunteerForceException extends Exception {}
} 