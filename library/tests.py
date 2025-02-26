from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from library.models import Book, Loan, User
import datetime

class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create test user and authenticate
        self.user = User.objects.create_user(
            email="admin@gmail.com", password="0000"
        )
        self.client.force_authenticate(user=self.user)

        # Create test book
        self.book = Book.objects.create(
            title="Django for Beginners", author="William S. Vincent", isbn="000-0-00-000000-0", page_count=250, available=True
        )

    def test_get_books_list(self):
        """Ensure we can retrieve the book list"""
        response = self.client.get(reverse("book-list"))

        print(response.data)  # Debugging output

        if "results" in response.data:  # If pagination is enabled
            books = response.data["results"]
        else:
            books = response.data  # If no pagination

        self.assertGreater(len(books), 0)  # Ensure books exist
        self.assertEqual(books[0]["title"], self.book.title)

    def test_create_book(self):
        """Ensure we can create a book"""
        data = {"title": "New Book", "author": "Jane Doe", "isbn": "123-4-56-789012-3", "page_count": 300, "available": True}
        response = self.client.post(reverse("book-list"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book(self):
        """Ensure we can update a book"""
        data = {"title": "Updated Book"}
        response = self.client.patch(reverse("book-detail", args=[self.book.id]), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book(self):
        """Ensure we can delete a book"""
        response = self.client.delete(reverse("book-detail", args=[self.book.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LoanAPITestCase(APITestCase):
    def setUp(self):
        # Create test user and authenticate
        self.user = User.objects.create_user(
            email="admin@gmail.com", password="0000"
        )
        self.client.force_authenticate(user=self.user)

        # Create test book
        self.book = Book.objects.create(
            title="Django Advanced", author="John Doe", isbn="123-4-56-789012-3", page_count=200, available=True
        )

        # Create a loan
        self.loan = Loan.objects.create(book=self.book, user=self.user)

    def test_create_loan(self):
        Loan.objects.filter(book=self.book, user=self.user).delete()

        data = {"book": self.book.id, "user": self.user.id}
        url = reverse("loan-borrow", kwargs={"pk": self.book.id})

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_return_loan(self):
        self.client.force_authenticate(user=self.user)

        url = reverse("loan-return-book", kwargs={"pk": self.loan.id})
        response = self.client.post(url, {"returned_at": "2025-02-26"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)