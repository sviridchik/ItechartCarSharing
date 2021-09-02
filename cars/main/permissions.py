from rest_framework.permissions import BasePermission

from .models import Profile


class MyPermissionAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        user_profile = Profile.objects.get(pk=user.id)
        if not user_profile.is_admin:
            return False
        else:
            return True


class MyPermissionPkME(BasePermission):
    def has_permission(self, request, view, pk=None, me=None):
        pk_user = request.user.id
        pk = view.kwargs.get('pk')
        me = view.kwargs.get('me')
        user_profile = Profile.objects.get(pk=pk_user)

        if pk is not None:
            pk = int(pk)
            # not me ,then admin
            if pk != pk_user:
                if not user_profile.is_admin:
                    return False
                else:
                    return True
            else:
                return True
        elif me is not None:
            return True
