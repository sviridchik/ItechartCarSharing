from rest_framework.permissions import BasePermission

from users.models import Profile

class MyPermissionAdminNotUser(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        user = request.user
        user_profile = Profile.objects.get(user=user)
        return user_profile.is_admin
