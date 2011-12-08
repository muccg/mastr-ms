from madas.users.user_manager import get_user_manager
from django.contrib.auth.backends import ModelBackend
from ccg.auth.backends import LDAPBackend
from madas.repository.models import MadasUser

class MadasBackend(ModelBackend):
    '''
    Returns a MadasUser that has group info etc instead of the plain Django User.
    This will result in request.user being an instance of MadasUser instead of User.
    '''
    supports_object_permissions = False
    supports_anonymous_user = False
    
    def get_groups(self, user):
        user_manager = get_user_manager()
        return user_manager.get_user_groups(user.username)

    def get_user(self, user_id):
        try:
            user = MadasUser.objects.get(pk=user_id)
            groups = self.get_groups(user)
            user.set_magroups(groups)
            return user
        except MadasUser.DoesNotExist:
            return None

