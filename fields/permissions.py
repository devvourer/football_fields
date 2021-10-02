from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """ Создавать футбольные поля могут только владельцы """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True

        return False
