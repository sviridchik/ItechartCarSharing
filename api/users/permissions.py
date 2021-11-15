from rest_framework.permissions import BasePermission

from users.models import Profile


class MyPermissionAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        user = request.user
        user_profile = Profile.objects.get(user = user)

        if not user_profile.is_admin:
            return False
        else:
            return True


class MyPermissionAge(BasePermission):
    message = 'Age should be >= 18'

    def has_permission(self, request, view):
        birth_date = Profile.objects.get(user=request.user).date_of_birth
        if (date.today() - birth_date) // timedelta(days=365.2425) < 18:
            return False
        else:
            return True


class MyPermissionPkME(BasePermission):
    def has_permission(self, request, view):
        user_profile = request.user.profile

        pk = view.kwargs.get('pk')
        me = view.kwargs.get('me')

        if me or str(user_profile.pk) == pk:
            return True
        if user_profile.is_admin:
            return True
        return False
