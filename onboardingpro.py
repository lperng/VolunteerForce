import networkx as nx
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import logging
import requests
from collections import defaultdict

class OnboardingProAgent:
    """
    OnboardingPro Agent for VolunteerForce
    
    This agent creates personalized onboarding experiences for volunteers
    based on their skills, role requirements, and learning preferences.
    """
    
    def __init__(self, sf_connection, lms_connection=None, config=None):
        """
        Initialize the OnboardingPro Agent
        
        Args:
            sf_connection: Salesforce API connection
            lms_connection: Learning Management System connection (optional)
            config: Configuration dictionary for the agent
        """
        self.sf = sf_connection
        self.lms = lms_connection
        self.config = config or self._default_config()
        self.logger = logging.getLogger('volunteerforce.onboardingpro')
        
        # Initialize training module graph
        self.training_graph = self._build_training_graph()
    
    def _default_config(self):
        """Default configuration settings"""
        return {
            'training': {
                'max_daily_hours': 2,
                'min_module_completion': 0.85,
                'reminder_days': [3, 1],  # Days before deadline to send reminders
                'escalation_threshold': 7  # Days past deadline to escalate
            },
            'certification': {
                'auto_verify': ['basic_orientation', 'safety_guidelines'],
                'expiration_warning_days': 30
            },
            'communication': {
                'channels': ['email', 'sms', 'app_notification'],
                'default_channel': 'app_notification'
            }
        }
    
    def _build_training_graph(self):
        """
        Build a directed graph of training modules with prerequisites
        
        Returns:
            NetworkX DiGraph of training modules
        """
        # Create directed graph
        G = nx.DiGraph()
        
        # Fetch training modules from Salesforce
        modules = self.sf.get_training_modules()
        
        # Add nodes for each module
        for module in modules:
            G.add_node(
                module['id'],
                name=module['name'],
                description=module['description'],
                duration_minutes=module['duration_minutes'],
                skill_category=module['skill_category'],
                difficulty=module['difficulty'],
                required_roles=module.get('required_roles', []),
                optional_roles=module.get('optional_roles', [])
            )
        
        # Add edges for prerequisites
        for module in modules:
            for prereq_id in module.get('prerequisites', []):
                G.add_edge(prereq_id, module['id'])
        
        return G
    
    def generate_learning_path(self, volunteer_id, role_id):
        """
        Generate a personalized learning path for a volunteer based on role
        
        Args:
            volunteer_id: Volunteer identifier
            role_id: Role identifier
            
        Returns:
            Dictionary with learning path information
        """
        # Get volunteer data
        volunteer = self.sf.get_volunteer(volunteer_id)
        if not volunteer:
            self.logger.error(f"Volunteer {volunteer_id} not found")
            return {"error": "Volunteer not found"}
        
        # Get role data
        role = self.sf.get_role(role_id)
        if not role:
            self.logger.error(f"Role {role_id} not found")
            return {"error": "Role not found"}
        
        # Get volunteer's completed trainings
        completed_trainings = self.sf.get_volunteer_trainings(volunteer_id)
        completed_module_ids = [
            t['module_id'] for t in completed_trainings 
            if t['status'] == 'Completed' and t['score'] >= self.config['training']['min_module_completion']
        ]
        
        # Get role's required and recommended skills
        required_skills = role.get('required_skills', [])
        recommended_skills = role.get('recommended_skills', [])
        
        # Get volunteer's existing skills
        volunteer_skills = volunteer.get('skills', [])
        
        # Identify required modules based on role
        required_modules = []
        recommended_modules = []
        
        for node, attrs in self.training_graph.nodes(data=True):
            # Skip modules already completed
            if node in completed_module_ids:
                continue
            
            # Check if module is required for the role
            if role_id in attrs.get('required_roles', []):
                required_modules.append(node)
            elif role_id in attrs.get('optional_roles', []):
                recommended_modules.append(node)
            elif attrs.get('skill_category') in required_skills and attrs.get('skill_category') not in volunteer_skills:
                required_modules.append(node)
            elif attrs.get('skill_category') in recommended_skills and attrs.get('skill_category') not in volunteer_skills:
                recommended_modules.append(node)
        
        # Find all prerequisites for required modules
        all_required = set(required_modules)
        for module in required_modules:
            # Find all predecessors (prerequisites) using networkx
            predecessors = list(nx.ancestors(self.training_graph, module))
            # Add prerequisites to required modules if not already completed
            for prereq in predecessors:
                if prereq not in completed_module_ids:
                    all_required.add(prereq)
        
        # Create a subgraph with required modules and their prerequisites
        path_graph = self.training_graph.subgraph(all_required)
        
        # Topologically sort to get proper sequence with prerequisites first
        try:
            module_sequence = list(nx.topological_sort(path_graph))
        except nx.NetworkXUnfeasible:
            # Handle cycles in the graph (should not happen with proper data)
            self.logger.error("Cycle detected in training module graph")
            module_sequence = list(all_required)
        
        # Add recommended modules at the end if they don't have unmet prerequisites
        for module in recommended_modules:
            # Check if all prerequisites are either completed or in the required path
            prereqs = list(self.training_graph.predecessors(module))
            prereqs_satisfied = all(
                prereq in completed_module_ids or prereq in all_required
                for prereq in prereqs
            )
            
            if prereqs_satisfied and module not in all_required:
                module_sequence.append(module)
        
        # Create learning path with module details and estimated completion dates
        learning_path = []
        current_date = datetime.now()
        accumulated_minutes = 0
        
        for module_id in module_sequence:
            module_attrs = self.training_graph.nodes[module_id]
            
            # Calculate estimated completion date
            duration_minutes = module_attrs.get('duration_minutes', 60)
            accumulated_minutes += duration_minutes
            
            # Assuming volunteers train up to max_daily_hours per day
            days_needed = accumulated_minutes / (self.config['training']['max_daily_hours'] * 60)
            estimated_completion = current_date + timedelta(days=int(days_needed))
            
            # Add module to learning path
            learning_path.append({
                'module_id': module_id,
                'name': module_attrs.get('name'),
                'description': module_attrs.get('description'),
                'duration_minutes': duration_minutes,
                'skill_category': module_attrs.get('skill_category'),
                'difficulty': module_attrs.get('difficulty'),
                'prerequisites': list(self.training_graph.predecessors(module_id)),
                'required': module_id in required_modules,
                'estimated_completion': estimated_completion.strftime('%Y-%m-%d')
            })
        
        # Create overall learning path information
        path_info = {
            'volunteer_id': volunteer_id,
            'role_id': role_id,
            'created_date': current_date.strftime('%Y-%m-%d'),
            'total_modules': len(learning_path),
            'required_modules': len(required_modules),
            'recommended_modules': len(learning_path) - len(required_modules),
            'estimated_hours': accumulated_minutes / 60,
            'modules': learning_path
        }
        
        # Save learning path to Salesforce
        path_id = self.sf.create_learning_path(path_info)
        path_info['path_id'] = path_id
        
        return path_info
    
    def track_training_progress(self, volunteer_id, path_id=None):
        """
        Track a volunteer's progress through their learning path
        
        Args:
            volunteer_id: Volunteer identifier
            path_id: Optional learning path identifier (gets latest if not provided)
            
        Returns:
            Dictionary with training progress information
        """
        # Get volunteer's learning path
        if path_id:
            path = self.sf.get_learning_path(path_id)
        else:
            # Get most recent learning path
            paths = self.sf.get_volunteer_learning_paths(volunteer_id)
            if not paths:
                return {"error": "No learning path found for volunteer"}
            path = paths[0]  # Most recent path
        
        # Get volunteer's completed trainings
        completed_trainings = self.sf.get_volunteer_trainings(volunteer_id)
        
        # Create mapping of module ID to completion status
        completion_status = {
            t['module_id']: {
                'status': t['status'],
                'completion_date': t['completion_date'],
                'score': t['score']
            }
            for t in completed_trainings
        }
        
        # Track progress for each module in the path
        modules_progress = []
        completed_count = 0
        total_modules = len(path['modules'])
        
        for module in path['modules']:
            module_id = module['module_id']
            status = completion_status.get(module_id, {'status': 'Not Started', 'score': 0})
            
            if status['status'] == 'Completed':
                completed_count += 1
            
            modules_progress.append({
                'module_id': module_id,
                'name': module['name'],
                'status': status['status'],
                'score': status.get('score', 0),
                'completion_date': status.get('completion_date'),
                'required': module['required'],
                'estimated_completion': module['estimated_completion']
            })
        
        # Calculate overall progress
        progress_percentage = (completed_count / total_modules) * 100 if total_modules > 0 else 0
        
        # Identify overdue modules
        current_date = datetime.now().strftime('%Y-%m-%d')
        overdue_modules = [
            m for m in modules_progress
            if m['status'] != 'Completed' 
            and m['estimated_completion'] < current_date
            and m['required']
        ]
        
        # Overall progress information
        progress_info = {
            'volunteer_id': volunteer_id,
            'path_id': path['path_id'],
            'progress_percentage': progress_percentage,
            'completed_modules': completed_count,
            'total_modules': total_modules,
            'overdue_modules': len(overdue_modules),
            'modules': modules_progress
        }
        
        return progress_info
    
    def recommend_resources(self, volunteer_id, module_id):
        """
        Recommend additional learning resources for a specific module
        
        Args:
            volunteer_id: Volunteer identifier
            module_id: Training module identifier
            
        Returns:
            List of recommended resources
        """
        # Get module details
        module = self.sf.get_training_module(module_id)
        if not module:
            return {"error": "Module not found"}
        
        # Get volunteer data to personalize recommendations
        volunteer = self.sf.get_volunteer(volunteer_id)
        if not volunteer:
            return {"error": "Volunteer not found"}
        
        # Get volunteer's learning style if available
        learning_style = volunteer.get('learning_preferences', {}).get('style', 'visual')
        
        # Get resources for this module
        resources = self.sf.get_module_resources(module_id)
        
        # Filter and rank resources based on volunteer's learning style
        style_match_resources = [r for r in resources if r.get('learning_style') == learning_style]
        other_resources = [r for r in resources if r.get('learning_style') != learning_style]
        
        # Combine with style matches first
        recommended = style_match_resources + other_resources
        
        # Limit to top 5 resources
        return recommended[:5]
    
    def schedule_follow_ups(self, volunteer_id, path_id=None):
        """
        Schedule automated follow-ups for incomplete training
        
        Args:
            volunteer_id: Volunteer identifier
            path_id: Optional learning path identifier (gets latest if not provided)
            
        Returns:
            Dictionary with scheduled follow-up information
        """
        # Get progress information
        progress = self.track_training_progress(volunteer_id, path_id)
        if 'error' in progress:
            return progress
        
        # Identify modules needing follow-up
        current_date = datetime.now()
        follow_ups = []
        
        for module in progress['modules']:
            if module['status'] == 'Completed':
                continue
            
            estimated_completion = datetime.strptime(module['estimated_completion'], '%Y-%m-%d')
            days_until_due = (estimated_completion - current_date).days
            
            # Schedule reminders based on config
            for reminder_days in self.config['training']['reminder_days']:
                if days_until_due == reminder_days:
                    follow_ups.append({
                        'module_id': module['module_id'],
                        'module_name': module['name'],
                        'type': 'reminder',
                        'scheduled_date': (current_date + timedelta(days=1)).strftime('%Y-%m-%d'),
                        'message': f"Reminder: Your training module '{module['name']}' is due in {reminder_days} days."
                    })
            
            # Schedule escalations for overdue modules
            if days_until_due < 0 and abs(days_until_due) >= self.config['training']['escalation_threshold']:
                follow_ups.append({
                    'module_id': module['module_id'],
                    'module_name': module['name'],
                    'type': 'escalation',
                    'scheduled_date': current_date.strftime('%Y-%m-%d'),
                    'message': f"Your training module '{module['name']}' is {abs(days_until_due)} days overdue."
                })
        
        # Create follow-up notifications in Salesforce
        for follow_up in follow_ups:
            notification = {
                'recipient_id': volunteer_id,
                'recipient_type': 'volunteer',
                'notification_type': follow_up['type'],
                'subject': f"Training {follow_up['type'].capitalize()}: {follow_up['module_name']}",
                'message': follow_up['message'],
                'scheduled_date': follow_up['scheduled_date'],
                'action_url': f"/volunteer/training/module/{follow_up['module_id']}",
                'priority': 'high' if follow_up['type'] == 'escalation' else 'medium'
            }
            
            notification_id = self.sf.schedule_notification(notification)
            follow_up['notification_id'] = notification_id
        
        return {
            'volunteer_id': volunteer_id,
            'path_id': progress['path_id'],
            'total_follow_ups': len(follow_ups),
            'reminders': sum(1 for f in follow_ups if f['type'] == 'reminder'),
            'escalations': sum(1 for f in follow_ups if f['type'] == 'escalation'),
            'follow_ups': follow_ups
        }
    
    def verify_certifications(self, volunteer_id):
        """
        Verify volunteer certifications and identify expiring ones
        
        Args:
            volunteer_id: Volunteer identifier
            
        Returns:
            Dictionary with certification status information
        """
        # Get volunteer certifications
        certifications = self.sf.get_volunteer_certifications(volunteer_id)
        
        # Get current date
        current_date = datetime.now()
        
        # Categorize certifications
        valid_certs = []
        expiring_certs = []
        expired_certs = []
        
        for cert in certifications:
            # Parse expiration date
            if cert.get('expiration_date'):
                expiration = datetime.strptime(cert['expiration_date'], '%Y-%m-%d')
                days_until_expiration = (expiration - current_date).days
                
                if days_until_expiration < 0:
                    # Already expired
                    expired_certs.append({
                        **cert,
                        'days_expired': abs(days_until_expiration)
                    })
                elif days_until_expiration <= self.config['certification']['expiration_warning_days']:
                    # Expiring soon
                    expiring_certs.append({
                        **cert,
                        'days_until_expiration': days_until_expiration
                    })
                else:
                    # Valid certification
                    valid_certs.append({
                        **cert,
                        'days_until_expiration': days_until_expiration
                    })
            else:
                # Non-expiring certification
                valid_certs.append(cert)
        
        # Send notifications for expiring certifications
        for cert in expiring_certs:
            notification = {
                'recipient_id': volunteer_id,
                'recipient_type': 'volunteer',
                'notification_type': 'certification_expiring',
                'subject': f"Certification Expiring: {cert['name']}",
                'message': f"Your certification '{cert['name']}' will expire in {cert['days_until_expiration']} days. " +
                           f"Please renew it to continue volunteering in roles requiring this certification.",
                'action_url': f"/volunteer/certifications/{cert['certification_id']}/renew",
                'priority': 'high' if cert['days_until_expiration'] <= 7 else 'medium'
            }
            
            self.sf.send_notification(notification)
        
        # Return certification status information
        return {
            'volunteer_id': volunteer_id,
            'valid_certifications': len(valid_certs),
            'expiring_certifications': len(expiring_certs),
            'expired_certifications': len(expired_certs),
            'certification_details': {
                'valid': valid_certs,
                'expiring': expiring_certs,
                'expired': expired_certs
            }
        }
    
    def get_onboarding_checklist(self, volunteer_id, project_id):
        """
        Generate a personalized onboarding checklist for a volunteer-project assignment
        
        Args:
            volunteer_id: Volunteer identifier
            project_id: Project identifier
            
        Returns:
            Dictionary with onboarding checklist items
        """
        # Get data
        volunteer = self.sf.get_volunteer(volunteer_id)
        project = self.sf.get_project(project_id)
        
        if not volunteer or not project:
            self.logger.error(f"Volunteer {volunteer_id} or Project {project_id} not found")
            return {"error": "Volunteer or Project not found"}
        
        # Get project role
        role_id = project.get('role_id')
        if not role_id:
            self.logger.error(f"No role defined for project {project_id}")
            return {"error": "Project role not defined"}
        
        # Generate learning path if not already created
        paths = self.sf.get_volunteer_learning_paths(volunteer_id)
        matching_paths = [p for p in paths if p.get('role_id') == role_id]
        
        if matching_paths:
            path = matching_paths[0]
        else:
            path = self.generate_learning_path(volunteer_id, role_id)
        
        # Create checklist with training modules
        checklist_items = []
        
        # Add orientation items
        checklist_items.append({
            'type': 'orientation',
            'name': 'Organization Introduction',
            'description': 'Introduction to the nonprofit organization and its mission',
            'estimated_minutes': 30,
            'required': True,
            'link': f"/volunteer/orientation/{project['organization_id']}"
        })
        
        checklist_items.append({
            'type': 'orientation',
            'name': 'Project Briefing',
            'description': f"Overview of the {project['name']} project and objectives",
            'estimated_minutes': 45,
            'required': True,
            'link': f"/volunteer/projects/{project_id}/overview"
        })
        
        # Add training modules from learning path
        for module in path.get('modules', []):
            checklist_items.append({
                'type': 'training',
                'name': module['name'],
                'description': module.get('description', ''),
                'estimated_minutes': module.get('duration_minutes', 60),
                'required': module.get('required', True),
                'link': f"/volunteer/training/module/{module['module_id']}",
                'due_date': module.get('estimated_completion')
            })
        
        # Add required certifications
        role = self.sf.get_role(role_id)
        required_certifications = role.get('required_certifications', [])
        
        for cert_id in required_certifications:
            cert = self.sf.get_certification(cert_id)
            if cert:
                # Check if volunteer already has this certification
                volunteer_certs = self.sf.get_volunteer_certifications(volunteer_id)
                has_cert = any(vc['certification_id'] == cert_id for vc in volunteer_certs)
                
                if not has_cert:
                    checklist_items.append({
                        'type': 'certification',
                        'name': cert['name'],
                        'description': cert.get('description', ''),
                        'estimated_minutes': cert.get('estimated_time_minutes', 90),
                        'required': True,
                        'link': f"/volunteer/certifications/{cert_id}"
                    })
        
        # Add equipment/resources items
        for resource in project.get('required_resources', []):
            checklist_items.append({
                'type': 'resource',
                'name': resource['name'],
                'description': resource.get('description', ''),
                'required': resource.get('required', True),
                'link': resource.get('resource_link')
            })
        
        # Create onboarding checklist in Salesforce
        checklist = {
            'volunteer_id': volunteer_id,
            'project_id': project_id,
            'role_id': role_id,
            'created_date': datetime.now().strftime('%Y-%m-%d'),
            'status': 'In Progress',
            'total_items': len(checklist_items),
            'completed_items': 0,
            'items': checklist_items
        }
        
        checklist_id = self.sf.create_onboarding_checklist(checklist)
        checklist['checklist_id'] = checklist_id
        
        return checklist
    
    def update_checklist_progress(self, checklist_id, completed_items=None):
        """
        Update progress on an onboarding checklist
        
        Args:
            checklist_id: Checklist identifier
            completed_items: Optional list of completed item indices
            
        Returns:
            Updated checklist information
        """
        # Get current checklist
        checklist = self.sf.get_onboarding_checklist(checklist_id)
        if not checklist:
            return {"error": "Checklist not found"}
        
        # If no completed items provided, recalculate based on current data
        if completed_items is None:
            # Get volunteer's completed trainings
            volunteer_id = checklist['volunteer_id']
            completed_trainings = self.sf.get_volunteer_trainings(volunteer_id)
            completed_module_ids = [
                t['module_id'] for t in completed_trainings 
                if t['status'] == 'Completed'
            ]
            
            # Get volunteer's certifications
            volunteer_certs = self.sf.get_volunteer_certifications(volunteer_id)
            completed_cert_ids = [vc['certification_id'] for vc in volunteer_certs]
            
            # Update checklist items
            for i, item in enumerate(checklist['items']):
                if item['type'] == 'training' and 'module_id' in item:
                    if item['module_id'] in completed_module_ids:
                        item['completed'] = True
                        item['completion_date'] = next(
                            (t['completion_date'] for t in completed_trainings if t['module_id'] == item['module_id']),
                            datetime.now().strftime('%Y-%m-%d')
                        )
                
                elif item['type'] == 'certification' and 'certification_id' in item:
                    if item['certification_id'] in completed_cert_ids:
                        item['completed'] = True
                        item['completion_date'] = next(
                            (c['issue_date'] for c in volunteer_certs if c['certification_id'] == item['certification_id']),
                            datetime.now().strftime('%Y-%m-%d')
                        )
        else:
            # Update specified items
            for index in completed_items:
                if 0 <= index < len(checklist['items']):
                    checklist['items'][index]['completed'] = True
                    checklist['items'][index]['completion_date'] = datetime.now().strftime('%Y-%m-%d')
        
        # Update completion count
        completed_count = sum(1 for item in checklist['items'] if item.get('completed', False))
        checklist['completed_items'] = completed_count
        
        # Update status if all required items are completed
        required_items = sum(1 for item in checklist['items'] if item.get('required', True))
        completed_required = sum(
            1 for item in checklist['items'] 
            if item.get('required', True) and item.get('completed', False)
        )
        
        if completed_required == required_items:
            checklist['status'] = 'Completed'
            checklist['completion_date'] = datetime.now().strftime('%Y-%m-%d')
        
        # Update checklist in Salesforce
        self.sf.update_onboarding_checklist(checklist)
        
        # Notify volunteer manager if checklist is completed
        if checklist['status'] == 'Completed':
            project = self.sf.get_project(checklist['project_id'])
            if project and 'manager_id' in project:
                notification = {
                    'recipient_id': project['manager_id'],
                    'recipient_type': 'staff',
                    'notification_type': 'onboarding_completed',
                    'subject': f"Onboarding Completed: {checklist['volunteer_name']}",
                    'message': f"{checklist['volunteer_name']} has completed all required onboarding steps for {project['name']}.",
                    'action_url': f"/staff/volunteers/{checklist['volunteer_id']}",
                    'priority': 'medium'
                }
                self.sf.send_notification(notification)
        
        return checklist