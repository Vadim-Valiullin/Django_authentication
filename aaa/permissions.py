from rest_framework import permissions

from aaa.models import Selection, Ads


class SelectionUpdatePermission(permissions.BasePermission):
    message = 'У вас нет прав на это действие'

    def has_permission(self, request, view):
        owner_id = Selection.objects.get(pk=view.kwargs["pk"]).owner_id
        if owner_id == request.user.id:
            return True
        return False


class AdsUpdatePermission(permissions.BasePermission):
    message = 'У вас нет прав на редактирование других объявлений'

    def has_permission(self, request, view):
        if request.user.role in ['moderator', 'admin']:
            return True
        author_id = Ads.objects.get(pk=view.kwargs["pk"]).author_id
        if author_id == request.user.id:
            return True
        return False
