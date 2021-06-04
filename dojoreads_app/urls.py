from django.urls import path
from . import views

urlpatterns = [
    path('', views.books),
    path('new_book', views.new_book_review),
    path('<int:book_id>', views.book_info, name="book_info"),
    path('delete/<int:review_id>', views.delete_review, name="delete_review"),
    path('add-review/<int:book_id>', views.add_review, name="add_review"),
    path('users/<int:user_id>', views.user_profile, name="user_profile"),
]