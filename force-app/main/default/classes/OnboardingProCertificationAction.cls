public class OnboardingProCertificationAction {
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
}