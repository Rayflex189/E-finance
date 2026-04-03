from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if hasattr(request.user, "userprofile") and not request.user.userprofile.is_completed:
                return redirect('reset_setting')   # force them to finish profile
            return redirect('dashboard')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func