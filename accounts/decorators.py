from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def role_required(allowed_roles):
    """
    Restricts a view to specific user roles.

    Usage: @role_required(['pm', 'admin'])

    Without this, authentication (are you logged in) is being
    conflated with authorization (are you allowed to see THIS).
    Login alone doesn't mean access to every view — that's the
    gap this closes.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.role not in allowed_roles:
                messages.error(request, "You don't have permission to view that page.")
                return redirect('dashboard_redirect')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator