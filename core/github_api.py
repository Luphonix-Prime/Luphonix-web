"""
Module for GitHub API integration to fetch repository information.
"""
import os
import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def get_repositories(username=None, limit=10):
    """
    Fetch repositories from GitHub API
    
    Args:
        username: GitHub username to fetch repositories from
        limit: Maximum number of repositories to fetch
        
    Returns:
        list: List of repositories or empty list if error occurs
    """
    username = username or settings.GITHUB_USERNAME
    token = settings.GITHUB_TOKEN
    
    # Set up headers with authentication if token is available
    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'
    
    try:
        # Make request to GitHub API
        url = f'https://api.github.com/users/{username}/repos'
        params = {
            'sort': 'updated',
            'direction': 'desc',
            'per_page': limit
        }
        
        response = requests.get(url, headers=headers, params=params)
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
        logger.error(f"GitHub API error: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error when fetching GitHub repositories: {str(e)}")
        return []
