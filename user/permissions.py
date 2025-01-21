from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

class IsAdmin(permissions.BasePermission):
    """
    Allows access only to admin users.

    Checks if the request user is authenticated and has a user type of 'ADMIN'.
    If not, it raises a PermissionDenied exception.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.user_type == "ADMIN":
            return True
        else:
            raise PermissionDenied("You do not have permission to perform this action!")
        
class IsInvestor(permissions.BasePermission):
    """
    Allows access only to Investor users.

    Checks if the request user is authenticated and has a user type of 'INVESTOR'.
    If not, it raises a PermissionDenied exception.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.user_type == "INVESTOR":
            return True
        else:
            raise PermissionDenied("You do not have permission to perform this action!")


class IsRegularUser(permissions.BasePermission):
    """
    Allows access only to regularusers.

    Checks if the request user is authenticated and has a user type of 'REGULARUSERr'.
    If not, it raises a PermissionDenied exception.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.user_type == "REGULARUSER":
            return True
        else:
            raise PermissionDenied("You do not have permission to perform this action!")