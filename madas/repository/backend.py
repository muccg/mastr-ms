from ccg.auth.ldap_helper import LDAPHandler
from ccg.auth.backends import LDAPBackend
from madas.repository.models import MadasUser

class MadasBackend(LDAPBackend):
    '''
    Returns a MadasUser that has group info etc instead of the plain Django User.
    This will result in request.user being an instance of MadasUser instead of User.
    '''
    supports_object_permissions = False
    supports_anonymous_user = False
    
    def get_ldap_groups(self, user):
        # Could cache here or at LDAPHandler level if necessary
        ld = LDAPHandler()
        return ld.ldap_get_user_groups(user.username)

    def get_user(self, user_id):
        try:
            user = MadasUser.objects.get(pk=user_id)
            groups = self.get_ldap_groups(user)
            user.set_ldap_groups(groups)
            return user
        except MadasUser.DoesNotExist:
            return None

