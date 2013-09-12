from django.http import HttpResponse, HttpResponseForbidden
from ccg.http import HttpResponseUnauthorized
from functools import wraps

def restricted_view(f, restriction):
    @wraps(f)
    def new_function(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseUnauthorized()

        if restriction(request.user):
            return f(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()
    return new_function


def nodereps_only(f):
    return restricted_view(f, lambda u: u.IsNodeRep)

def admins_only(f):
    return restricted_view(f, lambda u: u.IsAdmin)

def admins_or_nodereps(f):
    return restricted_view(f, lambda u: u.IsAdmin or u.IsNodeRep)

def authentication_required(f):
    return restricted_view(f, lambda u: u.IsLoggedIn)

def privileged_only(f):
    return restricted_view(f, lambda u: u.IsAdmin or u.IsNodeRep or u.IsMastrAdmin or u.IsProjectLeader)

def mastr_users_only(f):
    return restricted_view(f, lambda u: u.IsAdmin or u.IsMastrAdmin or u.IsProjectLeader or u.IsMastrStaff)
