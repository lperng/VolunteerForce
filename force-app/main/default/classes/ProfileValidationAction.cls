public class ProfileValidationAction {
    // Debug flag to return demo data instead of calling service
    public static Boolean DEBUG = true;
    
    @InvocableMethod(label='Validate Volunteer Profile' 
                     description='Validates volunteer profile completeness and returns profile data'
                     category='AgentForce - OnboardingPro')
    public static List<JsonResult> validateProfile(List<String> volunteerIds) {
        List<JsonResult> results = new List<JsonResult>();
        
        if (DEBUG) {
            // Return demo data for each request
            for (Integer i = 0; i < volunteerIds.size(); i++) {
                JsonResult result = new JsonResult();
                result.jsonResponse = getDemoProfileResponse();
                results.add(result);
            }
            return results;
        }
        
        // If not in debug mode, implement actual service call logic here
        for (String volunteerId : volunteerIds) {
            // This would be the actual service call in a real implementation
            // ProfileService.ProfileResponse response = ProfileService.validateProfile(volunteerId);
            
            // For now, return demo data even in non-debug mode since service isn't implemented
            JsonResult result = new JsonResult();
            result.jsonResponse = getDemoProfileResponse();
            results.add(result);
        }
        
        return results;
    }
    
    private static String getDemoProfileResponse() {
        return '{"volunteerId":"a0N8Z000000KoUYUA0",'
             + '"volunteerName":"Alex Martinez",'
             + '"email":"alex.martinez@example.com",'
             + '"phone":"(555) 123-4567",'
             + '"postalCode":"94105",'
             + '"startDate":"2023-09-15",'
             + '"location":{"latitude":37.7749,"longitude":-122.4194},'
             + '"profileCompletion":{'
             +   '"overallPercentage":85,'
             +   '"sections":['
             +     '{"name":"Personal Information","complete":true,"percentage":100},'
             +     '{"name":"Skills","complete":true,"percentage":100},'
             +     '{"name":"Interests","complete":true,"percentage":100},'
             +     '{"name":"Availability","complete":true,"percentage":100},'
             +     '{"name":"Learning Preferences","complete":false,"percentage":50},'
             +     '{"name":"Certifications","complete":false,"percentage":60}'
             +   '],'
             +   '"missingFields":["Learning Preferences - Preferred Resources", "Certification - CPR"]'
             + '},'
             + '"skills":["Project Management","Communication","Leadership","Web Development","Event Planning"],'
             + '"interests":["Education","Community Development","Environmental Conservation","Technology","Arts"],'
             + '"availability":{'
             +   '"weekdays":["Monday","Wednesday","Friday"],'
             +   '"timeSlots":["Morning","Evening"],'
             +   '"maxHoursPerWeek":10,'
             +   '"canVolunteerRemotely":true'
             + '},'
             + '"learningPreferences":{'
             +   '"preferredStyles":["Visual","Hands-on"],'
             +   '"preferredFormats":["Video","Interactive"],'
             +   '"pacePreference":"Self-paced"'
             + '},'
             + '"recommendations":['
             +   '{"type":"Profile Enhancement","description":"Add your CPR certification to unlock more volunteer opportunities"},'
             +   '{"type":"Learning Preferences","description":"Complete your learning preferences to get more customized training resources"},'
             +   '{"type":"Skills Development","description":"Consider adding public speaking to your skills based on your current volunteer roles"}'
             + ']'
             + '}';
    }
    
    public class JsonResult {
        @InvocableVariable(required=true)
        public String jsonResponse;
    }
}