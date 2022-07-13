from rest_framework import permissions


class IsSellerAndOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        return request.user.is_seller and obj.seller == request.user
