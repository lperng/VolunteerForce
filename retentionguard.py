import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import logging
from sklearn.ensemble import RandomForestClassifier
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
from collections import Counter

class RetentionGuardAgent:
    """
    RetentionGuard Agent for VolunteerForce
    
    This agent proactively monitors volunteer engagement patterns,
    identifies potential burnout, and suggests personalized retention
    strategies.
    """
    
    def __init__(self, sf_connection, config=None):
        """
        Initialize the RetentionGuard Agent
        
        Args:
            sf_connection: Salesforce API connection
            config: Configuration dictionary for the agent
        """
        self.sf = sf_connection
        self.config = config or self._default_config()
        self.logger = logging.getLogger('volunteerforce.retentionguard')
        
        # Initialize sentiment analyzer
        try:
            nltk.data.find('vader_lexicon')
        except LookupError:
            nltk.download('vader_lexicon')
        
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        
        # Initialize burnout prediction model
        self.burnout_model = self._initialize_burnout_model()
    
    def _default_config(self):
        """Default configuration settings"""
        return {
            'engagement': {
                'low_activity_threshold': 14,  # Days of inactivity considered concerning
                'high_load_threshold': 20,     # Hours per week considered high load
                'feedback_threshold': -0.2,    # Negative sentiment threshold
                'checkin_frequency': 30        # Days between regular check-ins
            },
            'recognition': {
                'hour_milestones': [10, 25, 50, 100, 250, 500, 1000],
                'project_milestones': [1, 5, 10, 25, 50],
                'year_milestones': [1, 2, 5, 10, 15, 20],
                'impact_highlight_frequency': 90  # Days between impact highlights
            },
            'intervention': {
                'risk_thresholds': {
                    'low': 0.3,
                    'medium': 0.6,
                    'high': 0.8
                },
                'reengagement_strategies': {
                    'low': ['achievement_highlight', 'impact_story', 'skill_development'],
                    'medium': ['role_adjustment', 'schedule_check', 'feedback_session'],
                    'high': ['personal_outreach', 'break_suggestion', 'recognition_event']
                }
            }
        }
    
    def _initialize_burnout_model(self):
        """
        Initialize the machine learning model for burnout prediction
        
        Returns:
            Scikit-learn model for burnout prediction
        """
        # In production, this would load a pre-trained model
        # For demo purposes, we'll create a new model
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=5,
            random_state=42
        )
        
        # We would normally train this model here, but for demo we'll
        # assume it's already trained when making predictions
        
        return model
    
    def _extract_engagement_features(self, volunteer_id, days_back=90):
        """
        Extract engagement features for a volunteer
        
        Args:
            volunteer_id: Volunteer identifier
            days_back: Number of days of history to analyze
            
        Returns:
            Dictionary of engagement features
        """
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        # Get volunteer activity data
        activities = self.sf.get_volunteer_activities(
            volunteer_id, 
            start_date.strftime('%Y-%m-%d'),
            end_date.strftime('%Y-%m-%d')
        )
        
        # Get feedback data
        feedback = self.sf.get_volunteer_feedback(
            volunteer_id,
            start_date.strftime('%Y-%m-%d'),
            end_date.strftime('%Y-%m-%d')
        )
        
        # Calculate activity metrics
        if activities:
            activity_dates = [datetime.strptime(a['date'], '%Y-%m-%d') for a in activities]
            hours_logged = sum(a.get('hours', 0) for a in activities)
            projects_count = len(set(a.get('project_id') for a in activities))
            
            # Activity frequency
            activity_freq = len(activity_dates) / days_back
            
            # Days since last activity
            if activity_dates:
                last_activity = max(activity_dates)
                days_since_last = (end_date - last_activity).days
            else:
                days_since_last = days_back
            
            # Weekly hours (average over the period)
            weekly_hours = (hours_logged / days_back) * 7
            
            # Calculate volatility (standard deviation of daily hours)
            daily_hours = {}
            for activity in activities:
                date = activity['date']
                hours = activity.get('hours', 0)
                daily_hours[date] = daily_hours.get(date, 0) + hours
            
            hours_volatility = np.std(list(daily_hours.values())) if daily_hours else 0
            
        else:
            # No activities in the period
            activity_freq = 0
            days_since_last = days_back
            weekly_hours = 0
            hours_logged = 0
            projects_count = 0
            hours_volatility = 0
        
        # Calculate feedback metrics
        if feedback:
            # Analyze sentiment of feedback comments
            sentiment_scores = []
            for item in feedback:
                if 'comments' in item and item['comments']:
                    score = self.sentiment_analyzer.polarity_scores(item['comments'])
                    sentiment_scores.append(score['compound'])
            
            # Average sentiment (-1 to 1 scale)
            avg_sentiment = np.mean(sentiment_scores) if sentiment_scores else 0
            
            # Satisfaction trends (is it improving or declining?)
            if len(feedback) >= 2:
                # Sort by date
                sorted_feedback = sorted(feedback, key=lambda x: x['date'])
                
                # Calculate trend (linear regression slope)
                x = list(range(len(sorted_feedback)))
                y = [float(f.get('satisfaction_score', 3)) for f in sorted_feedback]
                
                # Simple linear regression slope
                x_mean = np.mean(x)
                y_mean = np.mean(y)
                numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(len(x)))
                denominator = sum((x[i] - x_mean) ** 2 for i in range(len(x)))
                
                satisfaction_trend = numerator / denominator if denominator != 0 else 0
            else:
                satisfaction_trend = 0
        else:
            # No feedback in the period
            avg_sentiment = 0
            satisfaction_trend = 0
        
        # Combine features
        features = {
            'activity_frequency': activity_freq,
            'days_since_last_activity': days_since_last,
            'weekly_hours': weekly_hours,
            'hours_volatility': hours_volatility,
            'total_hours': hours_logged,
            'projects_count': projects_count,
            'feedback_sentiment': avg_sentiment,
            'satisfaction_trend': satisfaction_trend
        }
        
        return features
    
    def predict_burnout_risk(self, volunteer_id):
        """
        Predict burnout risk for a volunteer
        
        Args:
            volunteer_id: Volunteer identifier
            
        Returns:
            Dictionary with burnout risk assessment
        """
        # Get volunteer data
        volunteer = self.sf.get_volunteer(volunteer_id)
        if not volunteer:
            self.logger.error(f"Volunteer {volunteer_id} not found")
            return {"error": "Volunteer not found"}
        
        # Extract engagement features
        features = self._extract_engagement_features(volunteer_id)
        
        # Convert features to format expected by model
        feature_array = [
            features['activity_frequency'],
            features['days_since_last_activity'],
            features['weekly_hours'],
            features['hours_volatility'],
            features['feedback_sentiment'],
            features['satisfaction_trend']
        ]
        
        # Reshaping for scikit-learn
        X = np.array(feature_array).reshape(1, -1)
        
        # For demo purposes, we'll simulate a prediction
        # In production, this would use the trained model
        # risk_probability = self.burnout_model.predict_proba(X)[0, 1]
        
        # Simulate prediction based on features
        risk_factors = 0
        
        # Check for concerning signs
        if features['days_since_last_activity'] > self.config['engagement']['low_activity_threshold']:
            risk_factors += 1
        
        if features['weekly_hours'] > self.config['engagement']['high_load_threshold']:
            risk_factors += 1
        
        if features['feedback_sentiment'] < self.config['engagement']['feedback_threshold']:
            risk_factors += 1
        
        if features['satisfaction_trend'] < -0.1:
            risk_factors += 1
        
        if features['hours_volatility'] > 5:  # High variability in hours
            risk_factors += 0.5
        
        # Calculate risk probability (0-1 scale)
        risk_probability = min(risk_factors / 4, 1.0)
        
        # Determine risk level
        if risk_probability >= self.config['intervention']['risk_thresholds']['high']:
            risk_level = 'high'
        elif risk_probability >= self.config['intervention']['risk_thresholds']['medium']:
            risk_level = 'medium'
        elif risk_probability >= self.config['intervention']['risk_thresholds']['low']:
            risk_level = 'low'
        else:
            risk_level = 'minimal'
        
        # Generate risk factors explanation
        risk_factors_explanation = []
        
        if features['days_since_last_activity'] > self.config['engagement']['low_activity_threshold']:
            risk_factors_explanation.append(
                f"Inactivity: No activity recorded in {features['days_since_last_activity']} days"
            )
        
        if features['weekly_hours'] > self.config['engagement']['high_load_threshold']:
            risk_factors_explanation.append(
                f"High workload: Averaging {features['weekly_hours']:.1f} hours per week"
            )
        
        if features['feedback_sentiment'] < self.config['engagement']['feedback_threshold']:
            risk_factors_explanation.append(
                "Negative feedback: Recent communications show signs of frustration"
            )
        
        if features['satisfaction_trend'] < -0.1:
            risk_factors_explanation.append(
                "Declining satisfaction: Ratings have been trending downward"
            )
        
        # Get recommended intervention strategies
        if risk_level in self.config['intervention']['reengagement_strategies']:
            strategies = self.config['intervention']['reengagement_strategies'][risk_level]
        else:
            strategies = []
        
        # Create risk assessment
        assessment = {
            'volunteer_id': volunteer_id,
            'volunteer_name': volunteer.get('name', ''),
            'assessment_date': datetime.now().strftime('%Y-%m-%d'),
            'risk_probability': risk_probability,
            'risk_level': risk_level,
            'risk_factors': risk_factors_explanation,
            'engagement_metrics': features,
            'recommended_strategies': strategies
        }
        
        # Save assessment to Salesforce
        assessment_id = self.sf.create_burnout_assessment(assessment)
        assessment['assessment_id'] = assessment_id
        
        # Create alert for high-risk volunteers
        if risk_level == 'high':
            # Get volunteer's manager or coordinator
            assignments = self.sf.get_volunteer_assignments(volunteer_id)
            managers = set()
            
            for assignment in assignments:
                project_id = assignment.get('project_id')
                if project_id:
                    project = self.sf.get_project(project_id)
                    if project and 'manager_id' in project:
                        managers.add(project['manager_id'])
            
            # Send alert to each manager
            for manager_id in managers:
                alert = {
                    'recipient_id': manager_id,
                    'recipient_type': 'staff',
                    'notification_type': 'burnout_alert',
                    'subject': f"Burnout Risk Alert: {volunteer.get('name', '')}",
                    'message': f"High burnout risk detected for {volunteer.get('name', '')}. " +
                               f"Key factors: {', '.join(risk_factors_explanation)}. " +
                               f"Please review the assessment and recommended interventions.",
                    'action_url': f"/staff/volunteers/{volunteer_id}/retention",
                    'priority': 'high'
                }
                
                self.sf.send_notification(alert)
        
        return assessment
    
    def identify_achievements(self, volunteer_id):
        """
        Identify volunteer achievements eligible for recognition
        
        Args:
            volunteer_id: Volunteer identifier
            
        Returns:
            List of achievements to recognize
        """
        # Get volunteer data
        volunteer = self.sf.get_volunteer(volunteer_id)
        if not volunteer:
            self.logger.error(f"Volunteer {volunteer_id} not found")
            return {"error": "Volunteer not found"}
        
        # Get volunteer history
        start_date = volunteer.get('start_date')
        if not start_date:
            start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        
        # Get activities
        activities = self.sf.get_volunteer_activities(volunteer_id, start_date)
        
        # Get already recognized achievements to avoid duplicates
        recognized = self.sf.get_volunteer_recognitions(volunteer_id)
        recognized_types = [(r['type'], r.get('value')) for r in recognized]
        
        # Calculate metrics
        total_hours = sum(a.get('hours', 0) for a in activities)
        unique_projects = set(a.get('project_id') for a in activities if a.get('project_id'))
        projects_count = len(unique_projects)
        
        # Calculate tenure
        start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
        years_active = (datetime.now() - start_datetime).days / 365
        
        # List of new achievements
        achievements = []
        
        # Check hour milestones
        for milestone in self.config['recognition']['hour_milestones']:
            if total_hours >= milestone and ('hours', milestone) not in recognized_types:
                achievements.append({
                    'type': 'hours',
                    'value': milestone,
                    'name': f"{milestone} Hour Milestone",
                    'description': f"Contributed {milestone} hours of volunteer service"
                })
        
        # Check project milestones
        for milestone in self.config['recognition']['project_milestones']:
            if projects_count >= milestone and ('projects', milestone) not in recognized_types:
                achievements.append({
                    'type': 'projects',
                    'value': milestone,
                    'name': f"{milestone} Project Milestone",
                    'description': f"Contributed to {milestone} different volunteer projects"
                })
        
        # Check anniversary milestones
        for milestone in self.config['recognition']['year_milestones']:
            if years_active >= milestone and ('anniversary', milestone) not in recognized_types:
                achievements.append({
                    'type': 'anniversary',
                    'value': milestone,
                    'name': f"{milestone} Year Anniversary",
                    'description': f"Celebrating {milestone} year{'s' if milestone > 1 else ''} as a volunteer"
                })
        
        # Check for skill development
        trainings = self.sf.get_volunteer_trainings(volunteer_id)
        recently_completed = [
            t for t in trainings 
            if t['status'] == 'Completed' and 
            datetime.strptime(t['completion_date'], '%Y-%m-%d') > datetime.now() - timedelta(days=30)
        ]
        
        for training in recently_completed:
            skill_type = training.get('skill_category')
            if skill_type and ('skill', skill_type) not in recognized_types:
                achievements.append({
                    'type': 'skill',
                    'value': skill_type,
                    'name': f"New Skill: {skill_type}",
                    'description': f"Developed new skill in {skill_type}"
                })
        
        # Check for certifications
        certifications = self.sf.get_volunteer_certifications(volunteer_id)
        recent_certs = [
            c for c in certifications
            if datetime.strptime(c['issue_date'], '%Y-%m-%d') > datetime.now() - timedelta(days=30)
        ]
        
        for cert in recent_certs:
            cert_name = cert.get('name')
            if cert_name and ('certification', cert_name) not in recognized_types:
                achievements.append({
                    'type': 'certification',
                    'value': cert_name,
                    'name': f"New Certification: {cert_name}",
                    'description': f"Earned {cert_name} certification"
                })
        
        # Check for impact achievements
        # This would normally pull from project impact metrics
        # For demo purposes, we'll simulate this
        
        return {
            'volunteer_id': volunteer_id,
            'volunteer_name': volunteer.get('name', ''),
            'total_achievements': len(achievements),
            'achievements': achievements
        }
    
    def trigger_recognition(self, volunteer_id, achievement=None):
        """
        Trigger a recognition event for a volunteer
        
        Args:
            volunteer_id: Volunteer identifier
            achievement: Optional specific achievement to recognize
            
        Returns:
            Recognition event details
        """
        # If no specific achievement provided, find eligible achievements
        if not achievement:
            achievements_data = self.identify_achievements(volunteer_id)
            if 'error' in achievements_data:
                return achievements_data
            
            achievements = achievements_data.get('achievements', [])
            if not achievements:
                return {
                    'volunteer_id': volunteer_id,
                    'status': 'no_eligible_achievements'
                }
            
            # Select the most significant achievement
            # Priority: anniversary > hours > projects > skills > certifications
            type_priority = {
                'anniversary': 1,
                'hours': 2,
                'projects': 3,
                'skill': 4,
                'certification': 5
            }
            
            # Sort by type priority and then by value (higher values first)
            achievements.sort(
                key=lambda a: (
                    type_priority.get(a['type'], 10),
                    -a.get('value', 0) if isinstance(a.get('value'), (int, float)) else 0
                )
            )
            
            achievement = achievements[0]
        
        # Get volunteer data
        volunteer = self.sf.get_volunteer(volunteer_id)
        if not volunteer:
            self.logger.error(f"Volunteer {volunteer_id} not found")
            return {"error": "Volunteer not found"}
        
        # Create recognition notification
        notification = {
            'recipient_id': volunteer_id,
            'recipient_type': 'volunteer',
            'notification_type': 'achievement',
            'subject': f"Achievement Unlocked: {achievement['name']}",
            'message': f"Congratulations! You've earned recognition for {achievement['description']}.",
            'action_url': f"/volunteer/achievements",
            'priority': 'medium'
        }
        
        notification_id = self.sf.send_notification(notification)
        
        # Record the recognition in Salesforce
        recognition = {
            'volunteer_id': volunteer_id,
            'type': achievement['type'],
            'value': achievement.get('value'),
            'name': achievement['name'],
            'description': achievement['description'],
            'date': datetime.now().strftime('%Y-%m-%d'),
            'notification_id': notification_id
        }
        
        recognition_id = self.sf.create_recognition(recognition)
        recognition['recognition_id'] = recognition_id
        
        # Notify volunteer managers
        assignments = self.sf.get_volunteer_assignments(volunteer_id)
        managers = set()
        
        for assignment in assignments:
            project_id = assignment.get('project_id')
            if project_id:
                project = self.sf.get_project(project_id)
                if project and 'manager_id' in project:
                    managers.add(project['manager_id'])
        
        for manager_id in managers:
            manager_notification = {
                'recipient_id': manager_id,
                'recipient_type': 'staff',
                'notification_type': 'volunteer_achievement',
                'subject': f"Volunteer Achievement: {volunteer.get('name', '')}",
                'message': f"{volunteer.get('name', '')} has earned recognition for {achievement['description']}.",
                'action_url': f"/staff/volunteers/{volunteer_id}",
                'priority': 'low'
            }
            
            self.sf.send_notification(manager_notification)
        
        return {
            'volunteer_id': volunteer_id,
            'volunteer_name': volunteer.get('name', ''),
            'achievement': achievement,
            'recognition_id': recognition_id,
            'status': 'recognized'
        }
    
    def suggest_reengagement_strategies(self, volunteer_id, risk_level=None):
        """
        Suggest personalized reengagement strategies for a volunteer
        
        Args:
            volunteer_id: Volunteer identifier
            risk_level: Optional risk level (will assess if not provided)
            
        Returns:
            List of recommended reengagement strategies
        """
        # If risk level not provided, assess it
        if not risk_level:
            assessment = self.predict_burnout_risk(volunteer_id)
            if 'error' in assessment:
                return assessment
            
            risk_level = assessment['risk_level']
        
        # Get volunteer data
        volunteer = self.sf.get_volunteer(volunteer_id)
        if not