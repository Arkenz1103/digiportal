from django.shortcuts import redirect
from django.urls import reverse
from functools import wraps


class RoleRequiredMixin:
    """Mixin to check if user has required role"""
    required_role = None
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        if self.required_role and request.user.role != self.required_role:
            return redirect('login')
        
        return super().dispatch(request, *args, **kwargs)


def teacher_required(view_func):
    """Decorator to require teacher role"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        if request.user.role != 'teacher':
            return redirect('login')
        
        return view_func(request, *args, **kwargs)
    return wrapper


def student_required(view_func):
    """Decorator to require student role"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        if request.user.role != 'student':
            return redirect('login')
        
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    """Decorator to require admin role"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        if request.user.role != 'admin':
            return redirect('login')
        
        return view_func(request, *args, **kwargs)
    return wrapper
