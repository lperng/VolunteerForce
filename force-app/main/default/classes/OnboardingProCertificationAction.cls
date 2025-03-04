public class OnboardingProCertificationAction {
    @InvocableMethod(label='Verify Certifications' 
                     description='Verifies volunteer certifications and identifies expiring ones'
                     category='AgentForce - OnboardingPro')
    public static List<JsonResult> verifyCertifications(List<String> volunteerIds) {
        List<JsonResult> results = new List<JsonResult>();
        
        for (String volunteerId : volunteerIds) {
            OnboardingProService.CertificationResponse certResponse = OnboardingProService.verifyCertifications(volunteerId);
            
            JsonResult result = new JsonResult();
            result.jsonResponse = JSON.serialize(certResponse);
            results.add(result);
        }
        
        return results;
    }
    
    public class JsonResult {
        @InvocableVariable(required=true)
        public String jsonResponse;
    }
}