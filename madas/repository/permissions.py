
PermissionsByRoles = {
    'noderep': (
            ('Project', 'create'),
        )
}

class PermissionManager(object):
    def has_permission(self, user, action, model=None):
        if user.is_admin:
            return True

        model_name = model.__class__.__name__
        permission = (model_name, action)
        if (user.is_noderep and permission in PermissionsByRoles['noderep']):
            return True

        return False

