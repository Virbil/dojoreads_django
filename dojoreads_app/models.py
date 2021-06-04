from django.db import models
from login_reg_app.models import User

class Book_Manager(models.Manager):
    def duplicate_check(self, post_data):
        errors = {}
        duplicate = Book.objects.filter(title=post_data['title'])
        
        if duplicate:
            errors['title'] = "This title is already entered"

        return errors

class Author(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name="books_authored", on_delete = models.CASCADE)
    uploaded_by = models.ForeignKey(User, related_name="books_uploaded", on_delete = models.CASCADE) # OTM - the user who uploaded a given book
    # OTM book_reviews
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = Book_Manager()

class Review(models.Model):
    user_id = models.ForeignKey(User, related_name="user_reviews", on_delete = models.CASCADE) # OTM - the user who wrote a review
    book_id = models.ForeignKey(Book, related_name="book_reviews", on_delete = models.CASCADE) # OTM - the review on a given book
    review = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Reviewer: {self.user_id.first_name} {self.user_id.last_name} Rating: {self.rating}"