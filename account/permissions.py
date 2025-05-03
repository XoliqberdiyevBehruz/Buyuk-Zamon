from rest_framework.permissions import BasePermission
from rest_framework.exceptions import NotFound

class IsStaffUserOr404(BasePermission):
    '''
    Only staff users can access
    '''
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        raise NotFound()