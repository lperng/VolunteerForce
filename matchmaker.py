import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from datetime import datetime
import json
import logging

class MatchMakerAgent:
    """
    MatchMaker Agent for VolunteerForce
    
    This agent analyzes volunteer profiles and project requirements to create
    optimal matches using machine learning and natural language processing.
    """
    
    def __init__(self, sf_connection, config=None):
        """
        Initialize the MatchMaker Agent
        
        Args:
            sf_connection: Salesforce API connection
            config: Configuration dictionary for the agent
        """
        self.sf = sf_connection
        self.config = config or self._default_config()
        self.logger = logging.getLogger('volunteerforce.matchmaker')
        
        # Initialize NLP components
        self.skill_vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        # Load models and cached data
        self._load_models()
    
    def _default_config(self):
        """Default configuration settings"""
        return {
            'weights': {
                'skill_match': 0.6,
                'availability': 0.25,
                'location_proximity': 0.05,
                'past_performance': 0.1
            },
            'threshold': {
                'min_match_score': 0.65,
                'top_n_recommendations': 5
            },
            'cache_ttl': 3600  # seconds
        }
    
    def _load_models(self):
        """Load pre-trained models and cached data"""
        # In a real implementation, this would load saved models
        self.volunteer_skill_matrix = None
        self.project_skill_matrix = None
        
        # For demo purposes, we'll generate these on first use
        self.skill_corpus_trained = False
    
    def _extract_volunteer_features(self, volunteer):
        """
        Extract relevant features from volunteer profile
        
        Args:
            volunteer: Dictionary containing volunteer data
            
        Returns:
            Dictionary of extracted features
        """
        # Extract skills as a concatenated string for vectorization
        skills_text = ' '.join(volunteer.get('skills', []))
        
        # Extract availability as a structured object
        availability = self._parse_availability(volunteer.get('availability', {}))
        
        # Extract location for proximity calculation
        location = {
            'latitude': volunteer.get('latitude'),
            'longitude': volunteer.get('longitude'),
            'postal_code': volunteer.get('postal_code')
        }
        
        # Extract historical performance metrics
        performance = self._calculate_performance_score(
            volunteer.get('past_engagements', [])
        )
        
        return {
            'id': volunteer.get('id'),
            'name': volunteer.get('name'),
            'skills_text': skills_text,
            'skills_list': volunteer.get('skills', []),
            'availability': availability,
            'location': location,
            'performance_score': performance
        }
    
    def _extract_project_features(self, project):
        """
        Extract relevant features from project requirements
        
        Args:
            project: Dictionary containing project data
            
        Returns:
            Dictionary of extracted features
        """
        # Extract required skills as text
        required_skills_text = ' '.join(project.get('required_skills', []))
        required_skills_text += ' ' + project.get('description', '')
        
        # Extract schedule
        schedule = self._parse_schedule(project.get('schedule', {}))
        
        # Extract location
        location = {
            'latitude': project.get('latitude'),
            'longitude': project.get('longitude'),
            'postal_code': project.get('postal_code')
        }
        
        return {
            'id': project.get('id'),
            'name': project.get('name'),
            'required_skills_text': required_skills_text,
            'required_skills_list': project.get('required_skills', []),
            'schedule': schedule,
            'location': location,
            'min_commitment_hours': project.get('min_commitment_hours', 0)
        }
    
    def _parse_availability(self, availability):
        """
        Parse volunteer availability into a structured format
        
        Args:
            availability: Raw availability data
            
        Returns:
            Structured availability object
        """
        # Default empty availability structure
        structured = {
            'weekly': {
                'monday': [],
                'tuesday': [],
                'wednesday': [],
                'thursday': [],
                'friday': [],
                'saturday': [],
                'sunday': []
            },
            'exceptions': {
                'blackout_dates': [],
                'available_dates': []
            }
        }
        
        # If availability data is provided, parse it
        if availability:
            for day, time_slots in availability.get('weekly', {}).items():
                structured['weekly'][day.lower()] = time_slots
            
            # Parse exception dates
            for date_type, dates in availability.get('exceptions', {}).items():
                structured['exceptions'][date_type] = dates
        
        return structured
    
    def _parse_schedule(self, schedule):
        """
        Parse project schedule into a structured format
        
        Args:
            schedule: Raw schedule data
            
        Returns:
            Structured schedule object
        """
        # Default empty schedule structure
        structured = {
            'start_date': None,
            'end_date': None,
            'weekly': {
                'monday': [],
                'tuesday': [],
                'wednesday': [],
                'thursday': [],
                'friday': [],
                'saturday': [],
                'sunday': []
            },
            'specific_dates': []
        }
        
        # If schedule data is provided, parse it
        if schedule:
            structured['start_date'] = schedule.get('start_date')
            structured['end_date'] = schedule.get('end_date')
            
            for day, time_slots in schedule.get('weekly', {}).items():
                structured['weekly'][day.lower()] = time_slots
            
            structured['specific_dates'] = schedule.get('specific_dates', [])
        
        return structured
    
    def _calculate_performance_score(self, past_engagements):
        """
        Calculate a performance score based on past volunteer engagements
        
        Args:
            past_engagements: List of past volunteer engagements
            
        Returns:
            Performance score between 0.8 and 1.2
        """
        if not past_engagements:
            return 1.0  # Neutral score for new volunteers
        
        # Calculate metrics from past engagements
        reliability = np.mean([eng.get('reliability', 0.5) for eng in past_engagements])
        satisfaction = np.mean([eng.get('satisfaction', 0.5) for eng in past_engagements])
        impact = np.mean([eng.get('impact', 0.5) for eng in past_engagements])
        
        # Combine metrics with weights
        weighted_score = (reliability * 0.4) + (satisfaction * 0.3) + (impact * 0.3)
        
        # Scale to range 0.8 - 1.2
        scaled_score = 0.8 + (weighted_score * 0.4)
        
        return scaled_score
    
    def _calculate_skill_match(self, volunteer_features, project_features):
        """
        Calculate skill match score using NLP and cosine similarity
        
        Args:
            volunteer_features: Extracted volunteer features
            project_features: Extracted project features
            
        Returns:
            Skill match score between 0 and 1
        """
        # Train vectorizer if not already trained
        if not self.skill_corpus_trained:
            # Collect skill texts from all volunteers and projects
            all_texts = [v['skills_text'] for v in self.volunteer_features] + \
                       [p['required_skills_text'] for p in self.project_features]
            self.skill_vectorizer.fit(all_texts)
            self.skill_corpus_trained = True
        
        # Vectorize volunteer skills and project requirements
        volunteer_vector = self.skill_vectorizer.transform([volunteer_features['skills_text']])
        project_vector = self.skill_vectorizer.transform([project_features['required_skills_text']])
        
        # Calculate cosine similarity
        similarity = cosine_similarity(volunteer_vector, project_vector)[0][0]
        
        # Direct skill matching (bonus for exact matches)
        direct_matches = set(volunteer_features['skills_list']).intersection(
            set(project_features['required_skills_list'])
        )
        
        direct_match_bonus = len(direct_matches) / max(
            len(project_features['required_skills_list']), 1
        ) * 0.3
        
        # Final skill match score (capped at 1.0)
        skill_score = min(similarity + direct_match_bonus, 1.0)
        
        return skill_score
    
    def _calculate_availability_match(self, volunteer_availability, project_schedule):
        """
        Calculate availability match score
        
        Args:
            volunteer_availability: Structured volunteer availability
            project_schedule: Structured project schedule
            
        Returns:
            Availability match score between 0 and 1
        """
        match_score = 0.0
        total_days = 7
        days_with_overlap = 0
        
        # Check each day of the week for time slot overlaps
        for day in volunteer_availability['weekly']:
            volunteer_slots = volunteer_availability['weekly'][day]
            project_slots = project_schedule['weekly'][day]
            
            if not project_slots:
                # No project activity on this day
                continue
            
            if not volunteer_slots:
                # Volunteer not available on this day
                continue
            
            # Check for overlapping time slots
            overlap_found = False
            for p_slot in project_slots:
                p_start = datetime.strptime(p_slot['start'], '%H:%M').time()
                p_end = datetime.strptime(p_slot['end'], '%H:%M').time()
                
                for v_slot in volunteer_slots:
                    v_start = datetime.strptime(v_slot['start'], '%H:%M').time()
                    v_end = datetime.strptime(v_slot['end'], '%H:%M').time()
                    
                    # Check if slots overlap
                    if (v_start <= p_end) and (v_end >= p_start):
                        overlap_found = True
                        break
                
                if overlap_found:
                    break
            
            if overlap_found:
                days_with_overlap += 1
        
        # Calculate base availability score
        base_score = days_with_overlap / total_days
        
        # Check blackout dates against project dates
        if project_schedule['start_date'] and project_schedule['end_date']:
            # Convert to datetime objects
            project_start = datetime.strptime(project_schedule['start_date'], '%Y-%m-%d')
            project_end = datetime.strptime(project_schedule['end_date'], '%Y-%m-%d')
            
            # Check blackout dates
            blackout_conflict = False
            for blackout_date in volunteer_availability['exceptions']['blackout_dates']:
                blackout = datetime.strptime(blackout_date, '%Y-%m-%d')
                if project_start <= blackout <= project_end:
                    blackout_conflict = True
                    break
            
            # Penalize for blackout date conflicts
            if blackout_conflict:
                base_score *= 0.7
        
        return base_score
    
    def _calculate_location_match(self, volunteer_location, project_location):
        """
        Calculate location proximity score
        
        Args:
            volunteer_location: Volunteer location data
            project_location: Project location data
            
        Returns:
            Location match score between 0 and 1
        """
        # If either location is missing coordinates, fall back to postal code
        if (not volunteer_location['latitude'] or not volunteer_location['longitude'] or
            not project_location['latitude'] or not project_location['longitude']):
            
            # Simple postal code comparison (first 3 digits for proximity)
            vol_postal = volunteer_location['postal_code'][:3] if volunteer_location['postal_code'] else ''
            proj_postal = project_location['postal_code'][:3] if project_location['postal_code'] else ''
            
            if vol_postal and proj_postal and vol_postal == proj_postal:
                return 1.0
            elif vol_postal and proj_postal and vol_postal[:2] == proj_postal[:2]:
                return 0.8
            else:
                return 0.4  # Default medium-distance score when we can't calculate precisely
        
        # Calculate Haversine distance between coordinates
        lat1, lon1 = volunteer_location['latitude'], volunteer_location['longitude']
        lat2, lon2 = project_location['latitude'], project_location['longitude']
        
        # Convert to radians
        lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
        c = 2 * np.arcsin(np.sqrt(a))
        r = 6371  # Radius of earth in kilometers
        distance = c * r
        
        # Convert distance to score (inversely proportional)
        # Assuming 50km is the max reasonable distance (score = 0.1)
        # and 0km is perfect match (score = 1.0)
        max_distance = 50
        min_score = 0.1
        
        if distance >= max_distance:
            return min_score
        
        # Linear interpolation between 1.0 and min_score
        score = 1.0 - ((1.0 - min_score) * distance / max_distance)
        return score
    
    def calculate_match_score(self, volunteer, project):
        """
        Calculate overall match score between volunteer and project
        
        Args:
            volunteer: Volunteer data
            project: Project data
            
        Returns:
            Match score dictionary with overall score and component scores
        """
        # Extract features
        volunteer_features = self._extract_volunteer_features(volunteer)
        project_features = self._extract_project_features(project)
        
        # Calculate component scores
        skill_score = self._calculate_skill_match(
            volunteer_features, project_features
        )
        
        availability_score = self._calculate_availability_match(
            volunteer_features['availability'], project_features['schedule']
        )
        
        location_score = self._calculate_location_match(
            volunteer_features['location'], project_features['location']
        )
        
        # Apply weights from configuration
        weights = self.config['weights']
        weighted_skill = skill_score * weights['skill_match']
        weighted_availability = availability_score * weights['availability']
        weighted_location = location_score * weights['location_proximity']
        weighted_performance = volunteer_features['performance_score'] * weights['past_performance']
        
        # Calculate overall score
        overall_score = (weighted_skill + weighted_availability + weighted_location) * weighted_performance
        
        # Return detailed score breakdown
        return {
            'volunteer_id': volunteer['id'],
            'project_id': project['id'],
            'overall_score': overall_score,
            'component_scores': {
                'skill_match': skill_score,
                'availability_match': availability_score,
                'location_match': location_score,
                'performance_factor': volunteer_features['performance_score']
            }
        }
    
    def find_matches_for_project(self, project_id, top_n=None):
        """
        Find best matching volunteers for a specific project
        
        Args:
            project_id: Project identifier
            top_n: Number of top matches to return (default from config)
            
        Returns:
            List of top volunteer matches with scores
        """
        if top_n is None:
            top_n = self.config['threshold']['top_n_recommendations']
        
        # Get project data
        project = self.sf.get_project(project_id)
        if not project:
            self.logger.error(f"Project {project_id} not found")
            return []
        
        # Get all active volunteers
        volunteers = self.sf.get_active_volunteers()
        
        # Calculate match scores for all volunteers
        match_scores = []
        for volunteer in volunteers:
            score = self.calculate_match_score(volunteer, project)
            if score['overall_score'] >= self.config['threshold']['min_match_score']:
                match_scores.append(score)
        
        # Sort by overall score (descending)
        match_scores.sort(key=lambda x: x['overall_score'], reverse=True)
        
        # Return top N matches
        return match_scores[:top_n]
    
    def find_matches_for_volunteer(self, volunteer_id, top_n=None):
        """
        Find best matching projects for a specific volunteer
        
        Args:
            volunteer_id: Volunteer identifier
            top_n: Number of top matches to return (default from config)
            
        Returns:
            List of top project matches with scores
        """
        if top_n is None:
            top_n = self.config['threshold']['top_n_recommendations']
        
        # Get volunteer data
        volunteer = self.sf.get_volunteer(volunteer_id)
        if not volunteer:
            self.logger.error(f"Volunteer {volunteer_id} not found")
            return []
        
        # Get all active projects
        projects = self.sf.get_active_projects()
        
        # Calculate match scores for all projects
        match_scores = []
        for project in projects:
            score = self.calculate_match_score(volunteer, project)
            if score['overall_score'] >= self.config['threshold']['min_match_score']:
                match_scores.append(score)
        
        # Sort by overall score (descending)
        match_scores.sort(key=lambda x: x['overall_score'], reverse=True)
        
        # Return top N matches
        return match_scores[:top_n]
    
    def schedule_assignment(self, volunteer_id, project_id):
        """
        Schedule a volunteer for a project and send notifications
        
        Args:
            volunteer_id: Volunteer identifier
            project_id: Project identifier
            
        Returns:
            Success status and assignment details
        """
        # Get data
        volunteer = self.sf.get_volunteer(volunteer_id)
        project = self.sf.get_project(project_id)
        
        if not volunteer or not project:
            self.logger.error(f"Volunteer {volunteer_id} or Project {project_id} not found")
            return {"success": False, "error": "Volunteer or Project not found"}
        
        # Calculate match score to verify suitability
        match_score = self.calculate_match_score(volunteer, project)
        
        if match_score['overall_score'] < self.config['threshold']['min_match_score']:
            self.logger.warning(f"Match score {match_score['overall_score']} below threshold")
            return {
                "success": False, 
                "error": "Match score below threshold",
                "score": match_score
            }
        
        # Create assignment in Salesforce
        assignment = {
            "volunteer_id": volunteer_id,
            "project_id": project_id,
            "start_date": project['schedule']['start_date'],
            "end_date": project['schedule']['end_date'],
            "status": "Assigned",
            "match_score": match_score['overall_score']
        }
        
        assignment_id = self.sf.create_assignment(assignment)
        
        # Send notifications
        self._send_assignment_notifications(volunteer, project, assignment_id)
        
        return {
            "success": True,
            "assignment_id": assignment_id,
            "match_score": match_score
        }
    
    def _send_assignment_notifications(self, volunteer, project, assignment_id):
        """
        Send notifications about a new assignment
        
        Args:
            volunteer: Volunteer data
            project: Project data
            assignment_id: Assignment identifier
        """
        # Volunteer notification
        volunteer_message = {
            "recipient_id": volunteer['id'],
            "recipient_type": "volunteer",
            "notification_type": "assignment",
            "subject": f"New Volunteer Assignment: {project['name']}",
            "message": f"You have been matched with {project['name']}. " +
                      f"Please confirm your availability for this project.",
            "action_url": f"/volunteer/assignments/{assignment_id}",
            "priority": "high"
        }
        
        # Project manager notification
        manager_message = {
            "recipient_id": project['manager_id'],
            "recipient_type": "staff",
            "notification_type": "assignment",
            "subject": f"New Volunteer Assigned: {volunteer['name']}",
            "message": f"{volunteer['name']} has been matched with {project['name']}. " +
                      f"Review their profile and prepare for onboarding.",
            "action_url": f"/staff/assignments/{assignment_id}",
            "priority": "medium"
        }
        
        # Send notifications through Salesforce
        self.sf.send_notification(volunteer_message)
        self.sf.send_notification(manager_message)
        