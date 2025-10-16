"""
Simple Inertia.js adapter for Django
"""
import json
from django.http import JsonResponse
from django.shortcuts import render
from django.middleware.csrf import get_token


def render(request, component, props=None):
    """
    Render an Inertia response
    
    Args:
        request: Django request object
        component: Vue component name (e.g., 'Teacher/Home')
        props: Dictionary of props to pass to the component
    
    Returns:
        JsonResponse for Inertia requests, or HTML for initial page load
    """
    if props is None:
        props = {}
    
    # Add CSRF token to props
    props['csrf_token'] = get_token(request)
    
    # Add authenticated user info if available
    if request.user.is_authenticated:
        props['auth'] = {
            'user': {
                'id': request.user.id,
                'name': request.user.get_full_name() or request.user.username,
                'email': request.user.email,
                'role': getattr(request.user, 'role', None),
            }
        }
    
    page_data = {
        'component': component,
        'props': props,
        'url': request.path,
        'version': '1.0',
    }
    
    # Check if this is an Inertia request
    if request.headers.get('X-Inertia'):
        response = JsonResponse(page_data)
        response['X-Inertia'] = 'true'
        response['Vary'] = 'Accept'
        return response
    
    # Initial page load - return HTML with embedded page data
    from django.shortcuts import render as django_render
    return django_render(request, 'base.html', {
        'page': json.dumps(page_data)
    })


class InertiaMiddleware:
    """
    Middleware to handle Inertia.js requests
    """
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Handle Inertia redirects
        if (response.status_code in [301, 302] and 
            request.headers.get('X-Inertia')):
            response.status_code = 303
            response['X-Inertia-Location'] = response['Location']
        
        return response
