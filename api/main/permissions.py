from rest_framework.permissions import BasePermission

from .models import Profile


class MyPermissionAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        user = request.user
        profile = Profile.objects.get(user=user)
        user_profile = Profile.objects.get(pk=profile.id)
        # raise Exception(user.id, profile.u_id)
        # user_profile = Profile.objects.get(pk=user.uuid)

        if not user_profile.is_admin:
            return False
        else:
            return True


class MyPermissionPkME(BasePermission):
    def has_permission(self, request, view, pk=None, me=None):
        user = request.user
        user_profile = Profile.objects.get(user=user)
        # pk_user = request.user.id
        pk_user = user_profile.id
        pk = view.kwargs.get('pk')
        me = view.kwargs.get('me')
        # raise Exception(pk)
        # user_profile = Profile.objects.get(pk=pk_user)

        if pk is not None:
            # pk = int(pk)
            # not me ,then admin

            if pk != str(pk_user):
                if not user_profile.is_admin:
                    return False
                else:
                    return True
            else:
                return True
        elif me is not None:
            return True
