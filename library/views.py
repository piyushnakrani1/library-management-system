from datetime import timezone, datetime
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, generics, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Book, Loan
from .serializers import BookSerializer, LoanSerializer, LoginSerializer, UserSerializer
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    """View for user registration"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(APIView):
    """View for user login"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class CustomPagination(PageNumberPagination):
    """Custom pagination with page size control."""
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50

class BookViewSet(viewsets.ViewSet):
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["author", "isbn", "available"]
    search_fields = ["title", "author"]
    ordering_fields = ["created_at", "title"]
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), permissions.IsAdminUser()]

    def list(self, request):
        """List all books with filtering and pagination."""
        books = Book.objects.all().order_by('-created_at')

        for backend in self.filter_backends:
            books = backend().filter_queryset(request, books, self)

        paginator = self.pagination_class()
        paginated_books = paginator.paginate_queryset(books, request)
        serializer = BookSerializer(paginated_books, many=True)
        return paginator.get_paginated_response(serializer.data)


    def retrieve(self, request, pk=None):
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        return Response({"message": "Book deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class LoanViewSet(viewsets.ViewSet):
    """ViewSet for handling book borrowing and returning."""

    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        """List all loans for the authenticated user."""
        loans = Loan.objects.filter(user=request.user)
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def borrow(self, request, pk=None):
        """Allows an authenticated user to borrow a book."""
        book = get_object_or_404(Book, pk=pk)

        if not book.available:
            return Response({"error": "Book is not available."}, status=status.HTTP_400_BAD_REQUEST)

        if Loan.objects.filter(user=request.user, book=book, returned_at__isnull=True).exists():
            return Response({"error": "You have already borrowed this book."}, status=status.HTTP_400_BAD_REQUEST)

        Loan.objects.create(user=request.user, book=book)
        book.available = False
        book.save()

        return Response({"message": "Book borrowed successfully."}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        """Allows an authenticated user to return a borrowed book."""
        loan = Loan.objects.filter(user=request.user, book_id=pk, returned_at__isnull=True).first()

        if not loan:
            return Response({"error": "You have not borrowed this book or it has already been returned."}, status=status.HTTP_400_BAD_REQUEST)

        loan.returned_at = datetime.now()
        loan.save()

        loan.book.available = True
        loan.book.save()

        return Response({"message": "Book returned successfully."}, status=status.HTTP_200_OK)
