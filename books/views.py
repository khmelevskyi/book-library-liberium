"""
Views for Book API endpoints.
"""

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from loans.models import Loan
from loans.serializers import LoanSerializer
from loans.services import LoanService

from .filters import BookFilter
from .models import Book
from .permissions import IsAdminOrReadOnly
from .serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Book model.

    list: GET /books/ - List all books (with filtering and pagination)
    retrieve: GET /books/<id>/ - Get book details
    create: POST /books/ - Create a new book (admin only)
    update: PUT /books/<id>/ - Full update (all fields required, admin only)
    partial_update: PATCH /books/<id>/ - Partial update (only provided fields, admin only)
    destroy: DELETE /books/<id>/ - Delete a book (admin only)
    borrow: POST /books/<id>/borrow/ - Borrow a book (authenticated users)
    return: POST /books/<id>/return/ - Return a book (authenticated users)
    loan_history: GET /books/<id>/loan_history/ - Get loan history for a book (admin only)
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = BookFilter
    search_fields = ("title", "author", "isbn")
    ordering_fields = ("title", "author", "created_at", "page_count")
    ordering = ("-created_at",)

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAuthenticated],
        url_path="borrow",
        url_name="borrow",
    )
    def borrow(self, request, pk=None) -> Response:
        """
        Borrow a book. Book ID is taken from URL.
        POST /books/<id>/borrow/
        """
        book = self.get_object()
        try:
            loan = LoanService.borrow_book(user=request.user, book=book)
            return Response(
                {
                    "message": f'Book "{book.title}" borrowed successfully',
                    "loan_id": loan.id,
                    "borrowed_at": loan.borrowed_at,
                },
                status=status.HTTP_201_CREATED,
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAuthenticated],
        url_path="return",
        url_name="return_book",
    )
    def return_book(self, request, pk=None) -> Response:
        """
        Return a book. Book ID is taken from URL.
        POST /books/<id>/return/
        """
        book = self.get_object()
        try:
            loan = LoanService.return_book(user=request.user, book=book)
            return Response(
                {
                    "message": f'Book "{book.title}" returned successfully',
                    "loan_id": loan.id,
                    "returned_at": loan.returned_at,
                },
                status=status.HTTP_200_OK,
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=["get"],
        permission_classes=[IsAuthenticated],
        url_path="loan_history",
        url_name="loan_history",
    )
    def loan_history(self, request, pk=None) -> Response:
        """
        Get loan history for a book. Admin only.
        GET /books/<id>/loan_history/
        """
        if not request.user.is_staff:
            return Response(
                {"error": "Only admin users can view loan history for books."},
                status=status.HTTP_403_FORBIDDEN,
            )

        book = self.get_object()
        loans = Loan.objects.filter(book=book).order_by("-borrowed_at")
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data)
