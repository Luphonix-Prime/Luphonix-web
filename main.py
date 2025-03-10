import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import requests

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.environ.get("SESSION_SECRET", "luphonix-secret-key")

# Firebase configuration - will be passed to client-side
firebase_config = {
    "apiKey": os.environ.get("FIREBASE_API_KEY", "AIzaSyDsQm2dNtaKdRGQnYbJuMf3o2twbY_ORpo"),
    "authDomain": os.environ.get("FIREBASE_PROJECT_ID", "signup-login-realtime-7e107") + ".firebaseapp.com",
    "databaseURL": "https://signup-login-realtime-7e107-default-rtdb.firebaseio.com",
    "projectId": os.environ.get("FIREBASE_PROJECT_ID", "signup-login-realtime-7e107"),
    "storageBucket": os.environ.get("FIREBASE_PROJECT_ID", "signup-login-realtime-7e107") + ".firebasestorage.app",
    "messagingSenderId": "209493006193",
    "appId": os.environ.get("FIREBASE_APP_ID", "1:209493006193:web:bbf7b765d7faf280f508d0")
}

# Sample data for the website (will be replaced with Firebase data)
TEAM_MEMBERS = [
    {
        "id": "1",
        "name": "Alex Johnson",
        "position": "CEO & Founder",
        "bio": "Tech enthusiast with over 15 years of experience in software development and business leadership.",
        "image_url": None,
        "linkedin": "https://linkedin.com/",
        "github": "https://github.com/",
        "twitter": "https://twitter.com/",
        "order": 1
    },
    {
        "id": "2",
        "name": "Sarah Chen",
        "position": "CTO",
        "bio": "Full-stack developer with expertise in cloud architecture and AI/ML technologies.",
        "image_url": None,
        "linkedin": "https://linkedin.com/",
        "github": "https://github.com/",
        "twitter": None,
        "order": 2
    },
    {
        "id": "3",
        "name": "Michael Rodriguez",
        "position": "Lead Developer",
        "bio": "Backend specialist with a passion for scalable microservices and database optimization.",
        "image_url": None,
        "linkedin": "https://linkedin.com/",
        "github": "https://github.com/",
        "twitter": "https://twitter.com/",
        "order": 3
    },
    {
        "id": "4",
        "name": "Emma Wilson",
        "position": "UX/UI Designer",
        "bio": "Creative designer focused on creating intuitive, accessible and beautiful digital experiences.",
        "image_url": None,
        "linkedin": "https://linkedin.com/",
        "github": None,
        "twitter": "https://twitter.com/",
        "order": 4
    }
]

TECHNOLOGIES = [
    {
        "id": "1",
        "name": "React",
        "category": "frontend",
        "description": "Building responsive and interactive user interfaces",
        "icon_class": "fab fa-react",
        "order": 1
    },
    {
        "id": "2",
        "name": "Node.js",
        "category": "backend",
        "description": "Server-side JavaScript runtime environment",
        "icon_class": "fab fa-node-js",
        "order": 1
    },
    {
        "id": "3",
        "name": "Python",
        "category": "backend",
        "description": "Versatile language for web development, data analysis, and AI",
        "icon_class": "fab fa-python",
        "order": 2
    },
    {
        "id": "4", 
        "name": "MongoDB",
        "category": "database",
        "description": "NoSQL database for modern applications",
        "icon_class": "fas fa-database",
        "order": 1
    },
    {
        "id": "5",
        "name": "Firebase",
        "category": "backend",
        "description": "Real-time database and authentication platform",
        "icon_class": "fas fa-fire",
        "order": 3
    },
    {
        "id": "6",
        "name": "AWS",
        "category": "devops",
        "description": "Cloud computing platform for scalable infrastructure",
        "icon_class": "fab fa-aws",
        "order": 1
    },
    {
        "id": "7",
        "name": "Docker",
        "category": "devops",
        "description": "Containerization for consistent development environments",
        "icon_class": "fab fa-docker",
        "order": 2
    },
    {
        "id": "8",
        "name": "Flutter",
        "category": "mobile",
        "description": "Cross-platform mobile app development framework",
        "icon_class": "fas fa-mobile-alt",
        "order": 1
    }
]

PROJECTS = [
    {
        "id": "1",
        "name": "CloudSync Platform",
        "description": "A scalable cloud synchronization platform for enterprise data management with real-time collaboration features.",
        "image_url": None,
        "project_url": "https://example.com/cloudsync",
        "github_repo": "luphonix/cloud-sync",
        "technologies": ["1", "2", "4", "6"],
        "order": 1
    },
    {
        "id": "2", 
        "name": "EcoTrack Mobile App",
        "description": "Mobile application for tracking and reducing carbon footprint with gamification elements to encourage sustainable behaviors.",
        "image_url": None,
        "project_url": "https://example.com/ecotrack",
        "github_repo": "luphonix/eco-track",
        "technologies": ["3", "5", "8"],
        "order": 2
    },
    {
        "id": "3",
        "name": "DataViz Dashboard",
        "description": "Interactive data visualization dashboard for business analytics with customizable widgets and real-time updates.",
        "image_url": None,
        "project_url": "https://example.com/dataviz",
        "github_repo": "luphonix/data-viz",
        "technologies": ["1", "3", "5", "7"],
        "order": 3
    }
]

def get_technology_by_id(tech_id):
    for tech in TECHNOLOGIES:
        if tech["id"] == tech_id:
            return tech
    return None

def get_technologies_for_project(project):
    project_techs = []
    for tech_id in project["technologies"]:
        tech = get_technology_by_id(tech_id)
        if tech:
            project_techs.append(tech)
    return project_techs

def get_github_repositories(username="luphonix", limit=6):
    """
    Fetch repositories from GitHub API
    
    Args:
        username: GitHub username to fetch repositories from
        limit: Maximum number of repositories to fetch
        
    Returns:
        list: List of repositories or empty list if error occurs
    """
    try:
        # Make request to GitHub API
        url = f'https://api.github.com/users/{username}/repos'
        params = {
            'sort': 'updated',
            'direction': 'desc',
            'per_page': limit
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        repos = response.json()
        
        # Process repositories to extract needed information
        processed_repos = []
        for repo in repos:
            processed_repos.append({
                'name': repo['name'],
                'description': repo['description'] or "No description available",
                'url': repo['html_url'],
                'stars': repo['stargazers_count'],
                'forks': repo['forks_count'],
                'language': repo['language'] or "Not specified",
                'updated_at': repo['updated_at'],
            })
        
        return processed_repos
        
    except requests.exceptions.RequestException as e:
        print(f"GitHub API error: {str(e)}")
        # Return fallback data for development
        return [
            {
                'name': 'cloud-sync',
                'description': 'A scalable cloud synchronization platform for enterprise data',
                'url': 'https://github.com/luphonix/cloud-sync',
                'stars': 45,
                'forks': 12,
                'language': 'JavaScript',
                'updated_at': '2024-10-15T10:30:00Z',
            },
            {
                'name': 'eco-track',
                'description': 'Mobile application for tracking and reducing carbon footprint',
                'url': 'https://github.com/luphonix/eco-track',
                'stars': 32,
                'forks': 8,
                'language': 'Dart',
                'updated_at': '2024-09-20T14:15:00Z',
            },
            {
                'name': 'data-viz',
                'description': 'Interactive data visualization dashboard for business analytics',
                'url': 'https://github.com/luphonix/data-viz',
                'stars': 28,
                'forks': 6,
                'language': 'Python',
                'updated_at': '2024-08-05T09:45:00Z',
            }
        ]
    except Exception as e:
        print(f"Unexpected error when fetching GitHub repositories: {str(e)}")
        return []

# Routes
@app.route('/')
def index():
    """Main landing page view"""
    # Get 4 team members, 8 technologies, and 3 projects for homepage
    team_members = sorted(TEAM_MEMBERS, key=lambda x: x["order"])[:4]
    technologies = sorted(TECHNOLOGIES, key=lambda x: (x["category"], x["order"]))[:8]
    projects = sorted(PROJECTS, key=lambda x: x["order"])[:3]
    
    # Add technologies to projects
    for project in projects:
        project["tech_objects"] = get_technologies_for_project(project)
    
    return render_template(
        'index.html',
        team_members=team_members,
        technologies=technologies,
        featured_projects=projects,
        firebase_api_key=firebase_config["apiKey"],
        firebase_project_id=firebase_config["projectId"],
        firebase_app_id=firebase_config["appId"],
    )

@app.route('/team')
def team():
    """Team members list view"""
    team_members = sorted(TEAM_MEMBERS, key=lambda x: x["order"])
    return render_template(
        'team.html',
        team_members=team_members,
        firebase_api_key=firebase_config["apiKey"],
        firebase_project_id=firebase_config["projectId"],
        firebase_app_id=firebase_config["appId"],
    )

@app.route('/technologies')
def technologies():
    """Technologies/Skills list view"""
    # Group technologies by category
    technologies_by_category = {}
    for category in ["frontend", "backend", "database", "devops", "mobile", "other"]:
        technologies_by_category[category] = [tech for tech in TECHNOLOGIES if tech["category"] == category]
    
    return render_template(
        'technologies.html',
        technologies=TECHNOLOGIES,
        technologies_by_category=technologies_by_category,
        firebase_api_key=firebase_config["apiKey"],
        firebase_project_id=firebase_config["projectId"],
        firebase_app_id=firebase_config["appId"],
    )

@app.route('/projects')
def projects():
    """Projects view with GitHub integration"""
    projects_list = sorted(PROJECTS, key=lambda x: x["order"])
    
    # Add technologies to projects
    for project in projects_list:
        project["tech_objects"] = get_technologies_for_project(project)
    
    # Get repositories from GitHub
    github_repos = get_github_repositories(limit=6)
    
    return render_template(
        'projects.html',
        projects=projects_list,
        github_repos=github_repos,
        firebase_api_key=firebase_config["apiKey"],
        firebase_project_id=firebase_config["projectId"],
        firebase_app_id=firebase_config["appId"],
    )

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact form view"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        # In a real application, you'd store this in Firebase and/or send an email
        # For now, just flash a success message
        flash("Your message has been sent successfully. We'll get back to you soon!", "success")
        return redirect(url_for('contact'))
    
    return render_template(
        'contact.html',
        firebase_api_key=firebase_config["apiKey"],
        firebase_project_id=firebase_config["projectId"],
        firebase_app_id=firebase_config["appId"],
    )

@app.route('/login')
def login():
    """Login page for Firebase Authentication"""
    return render_template(
        'login.html',
        firebase_api_key=firebase_config["apiKey"],
        firebase_project_id=firebase_config["projectId"],
        firebase_app_id=firebase_config["appId"],
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)