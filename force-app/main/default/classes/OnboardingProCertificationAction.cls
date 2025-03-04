public class OnboardingProCertificationAction {
    @InvocableMethod(label='Verify Certifications' 
                     description='Verifies volunteer certifications and identifies expiring ones'
                     category='AgentForce - OnboardingPro')
    public static List<CertificationResult> verifyCertifications(List<String> volunteerIds) {
        List<CertificationResult> results = new List<CertificationResult>();
        
        for (String volunteerId : volunteerIds) {
            CertificationResult result = new CertificationResult();
            result.certificationResponse = OnboardingProService.verifyCertifications(volunteerId);
            results.add(result);
        }
        
        return results;
    }
    
    public class CertificationResult {
        @InvocableVariable(required=true)
        public OnboardingProService.CertificationResponse certificationResponse;
    }
}