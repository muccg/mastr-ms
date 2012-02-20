from django.http import HttpResponse, HttpResponseForbidden
from ccg.http import HttpResponseUnauthorized
from mastrms.users.MAUser import MAUser

def restricted_view(f, restriction):
    def new_function(*args, **kwargs):
        request = args[0]
        if not request.user.is_authenticated():
            return HttpResponseUnauthorized()
        mauser = request.session.get('mauser', None)

        if mauser is None:
            mauser = MAUser()
            mauser.refresh()
            mauser = request.session.get('mauser', None)

        if restriction(mauser):
            return f(*args, **kwargs)
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

