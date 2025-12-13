"""
Views for user authentication and management.
"""
from django.contrib.auth import get_user_model
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from loans.models import Loan
from loans.serializers import LoanSerializer

from .permissions import IsAdminOrSelf
from .serializers import CustomTokenObtainPairSerializer, RegisterSerializer, UserSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    User registration endpoint.
    POST /auth/register/
    """
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs) -> Response:
        """Create a new user account."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                'message': 'User registered successfully',
                'user': UserSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(TokenObtainPairView):
    """
    User login endpoint.
    POST /auth/login/
    Returns JWT access and refresh tokens.
    """
    serializer_class = CustomTokenObtainPairSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request) -> Response:
    """
    Get current authenticated user information.
    GET /auth/me/
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for User model (read-only).

    list: GET /users/ - List all users (admin only)
    retrieve: GET /users/<id>/ - Get user details
        - Admin can view any user
        - Authenticated users can only view themselves
        - Anonymous users cannot access
    loan_history: GET /users/<id>/loan_history/ - Get loan history for a user
        - Admin can view any user's loan history
        - Authenticated users can only view their own loan history
        - Anonymous users cannot access
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdminOrSelf)

    def list(self, request, *args, **kwargs):
        """List all users - admin only."""
        if not request.user.is_staff:
            return Response(
                {'error': 'Only admin users can list all users.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        """Return queryset based on user permissions."""
        # Handle Swagger schema generation
        if getattr(self, 'swagger_fake_view', False):
            return User.objects.none()

        # Check if user is authenticated (not AnonymousUser)
        if not self.request.user.is_authenticated:
            return User.objects.none()

        # Admin can see all users
        if self.request.user.is_staff:
            return User.objects.all()
        # Regular users can only see themselves
        return User.objects.filter(id=self.request.user.id)

    @action(
        detail=True,
        methods=['get'],
        permission_classes=[IsAuthenticated, IsAdminOrSelf],
        url_path='loan_history',
        url_name='loan_history',
    )
    def loan_history(self, request, pk=None) -> Response:
        """
        Get loan history for a user.
        GET /users/<id>/loan_history/

        - Admin users can view any user's loan history
        - Authenticated users can only view their own loan history
        - Anonymous users cannot access this endpoint
        """
        user = self.get_object()

        # Check permissions: admin can see anyone, regular users can only see themselves
        if not request.user.is_staff and request.user.id != user.id:
            return Response(
                {'error': 'You can only view your own loan history.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        loans = Loan.objects.filter(user=user).order_by('-borrowed_at')
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data)
