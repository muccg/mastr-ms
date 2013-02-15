from mastrms.users.user_manager import get_user_manager
from django.contrib.auth.backends import ModelBackend
#from ccg.auth.backends import LDAPBackend
from mastrms.repository.models import MadasUser
print 'Madas Backend loaded'
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
        print 'repository backend is getting user'
        try:
            print 'repository backend is getting user'
            user = MadasUser.objects.get(pk=user_id)
            groups = self.get_groups(user)
            user.set_magroups(groups)
            return user
        except MadasUser.DoesNotExist:
            print 'repository backend could not find user'
            return None

