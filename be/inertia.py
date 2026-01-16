"""
Simple Inertia.js-like render function for Django
This provides a basic render function that returns JSON responses for SPA navigation
"""
from django.http import JsonResponse
from django.shortcuts import render as django_render


def render(request, component, props=None):
    """
    Render function that returns either HTML or JSON based on request type.
    For Inertia.js-style SPA navigation.
    """
    if props is None:
        props = {}
    
    # Check if this is an Inertia request (XHR with X-Inertia header)
    is_inertia = request.headers.get('X-Inertia', False)
    
    if is_inertia:
        # Return JSON for Inertia requests
        return JsonResponse({
            'component': component,
            'props': props,
            'url': request.path,
        })
    
    # For regular requests, return the base template
    # The Vue app will handle routing on the client side
    return django_render(request, 'index.html', {
        'component': component,
        'props': props,
    })


class InertiaMiddleware:
    """
    Middleware for handling Inertia.js requests.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response
