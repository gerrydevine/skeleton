from django.core.exceptions import PermissionDenied
from .models import Record

def user_is_record_owner(view_func):
    def wrap(request, *args, **kwargs):
        record = Record.objects.get(pk=kwargs["pk"])
        if record.owner == request.user:
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = view_func.__doc__
    wrap.__name__ = view_func.__name__
    return wrap
