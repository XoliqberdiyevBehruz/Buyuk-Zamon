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
    

class IsBoss(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'boss':
            return True
        else:
            return False
        

class IsBossOrEmployee(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role == 'boss' or request.user.role == 'employee':
                return True
        else:
            return False