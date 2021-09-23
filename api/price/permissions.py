from rest_framework.permissions import BasePermission

from users.models import Profile


class MyPermissionAdminNotUser(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        user = request.user
        user_profile = Profile.objects.get(user=user)

        if not user_profile.is_admin:
            return False
        else:
            return True


class MyPermissionPkME(BasePermission):
    def has_permission(self, request, view):
        user_profile = Profile.objects.get(user=request.user)

        pk = view.kwargs.get('pk')
        me = view.kwargs.get('me')

        if me or str(user_profile.pk) == pk:
            return True
        if user_profile.is_admin:
            return True
        return False
