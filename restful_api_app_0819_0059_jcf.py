# 代码生成时间: 2025-08-19 00:59:14
from django.db import models
from django.http import JsonResponse
from django.urls import path
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator

# Define the models
class Book(models.Model):
    """
    Represents a book with title and author.
    """
    title = models.CharField(max_length=200, help_text="The title of the book.")
    author = models.CharField(max_length=100, help_text="The author of the book.")
    def __str__(self):
        return self.title

# Define the views
class BookListView(View):
    """
    A view to list all books.
    """
    def get(self, request):
        """
        Return a JSON response containing all books.
        """
        books = Book.objects.all().values()
        return JsonResponse(list(books), safe=False)

    def post(self, request):
        """
        Create a new book instance.
        """
        data = request.POST
        book = Book(title=data['title'], author=data['author'])
        book.save()
        return JsonResponse({'id': book.id, 'title': book.title, 'author': book.author}, status=201)

class BookDetailView(View):
    """
    A view to retrieve, update or delete a specific book.
    """
    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return None

    def get(self, request, pk):
        book = self.get_object(pk)
        if book is not None:
            return JsonResponse(book.__dict__)
        else:
            return JsonResponse({'error': 'Book not found'}, status=404)

    def put(self, request, pk):
        """
        Update a book instance.
        """
        book = self.get_object(pk)
        if book is not None:
            book.title = request.POST.get('title', book.title)
            book.author = request.POST.get('author', book.author)
            book.save()
            return JsonResponse(book.__dict__)
        else:
            return JsonResponse({'error': 'Book not found'}, status=404)

    def delete(self, request, pk):
        book = self.get_object(pk)
        if book is not None:
            book.delete()
            return JsonResponse({'message': 'Book deleted'}, status=204)
        else:
            return JsonResponse({'error': 'Book not found'}, status=404)

# Define the URL patterns
urlpatterns = [
    path('books/', csrf_exempt(BookListView.as_view()), name='book-list'),
    path('books/<int:pk>/', csrf_exempt(BookDetailView.as_view()), name='book-detail'),
]
