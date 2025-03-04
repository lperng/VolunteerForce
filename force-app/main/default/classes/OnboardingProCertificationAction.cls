public class OnboardingProCertificationAction {
    // Debug flag to return demo data instead of calling service
    public static Boolean DEBUG = true;
    
    @InvocableMethod(label='Verify Certifications' 
                     description='Verifies volunteer certifications and identifies expiring ones'
                     category='AgentForce - OnboardingPro')
    public static List<JsonResult> verifyCertifications(List<String> volunteerIds) {
        List<JsonResult> results = new List<JsonResult>();
        
        if (DEBUG) {
            // Return demo data for each request
            for (Integer i = 0; i < volunteerIds.size(); i++) {
                JsonResult result = new JsonResult();
                result.jsonResponse = getDemoCertificationResponse();
                results.add(result);
            }
            return results;
        }
        
        // Original implementation
        for (String volunteerId : volunteerIds) {
            OnboardingProService.CertificationResponse certResponse = OnboardingProService.verifyCertifications(volunteerId);
            
            JsonResult result = new JsonResult();
            result.jsonResponse = JSON.serialize(certResponse);
            results.add(result);
        }
        
        return results;
    }
    
    private static String getDemoCertificationResponse() {
        return '{"volunteerName":"Jane Smith","validCertifications":[{"id":"a0M8Z000000JnUYUA0","name":"First Aid","issueDate":"2023-01-15","expirationDate":"2025-01-15","status":"Valid"},{"id":"a0M8Z000000JnUZUA0","name":"Crisis Management","issueDate":"2023-03-20","expirationDate":"2025-03-20","status":"Valid"}],"expiringCertifications":[{"id":"a0M8Z000000JnUaUA0","name":"CPR","issueDate":"2022-05-10","expirationDate":"2024-05-10","status":"Expiring Soon","daysUntilExpiration":45}],"missingCertifications":[{"name":"Safety Training","requiredFor":["Disaster Response","Emergency Shelter Volunteer"]}]}';
    }
    
    public class JsonResult {
        @InvocableVariable(required=true)
        public String jsonResponse;
    }
}