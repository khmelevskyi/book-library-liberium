"""
Views for Loan API endpoints.
"""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Loan
from .serializers import LoanSerializer


class LoanViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Loan model (read-only).

    list: GET /loans/ - List all loans for the authenticated user
    retrieve: GET /loans/<id>/ - Get loan details
    """

    serializer_class = LoanSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return loans for the authenticated user only."""
        # Handle Swagger schema generation
        if getattr(self, "swagger_fake_view", False):
            return Loan.objects.none()

        # Check if user is authenticated (not AnonymousUser)
        if not self.request.user.is_authenticated:
            return Loan.objects.none()

        return Loan.objects.filter(user=self.request.user)
