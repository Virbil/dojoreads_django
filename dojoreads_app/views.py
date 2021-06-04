from django.contrib import messages
from dojoreads_app.models import *
from django.shortcuts import render, redirect

def books(request):
    context = {
        "user_info": User.objects.get(id=request.session["userid"]),
        "all_books": Book.objects.all(),
        "recent_books": Book.objects.order_by("-created_at")[:3],
        "all_reviews": Review.objects.all()
    }
    return render(request, "books.html", context)

def new_book_review(request):
    if request.method == "POST":
        errors = Book.objects.duplicate_check(request.POST)

        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')

        logged_user = User.objects.get(id=request.session["userid"])

        author = Author.objects.create(
            name = request.POST["author_name"]
        )

        book = Book.objects.create(
            title = request.POST["title"],
            author = Author.objects.get(id = author.id),
            uploaded_by = logged_user
        )

        review = Review.objects.create(
            user_id = logged_user,
            book_id = Book.objects.get(id = book.id),
            review = request.POST["review"],
            rating = request.POST["rating"]
        )

        return redirect('/books')
    else:
        context = {
        "user_info": User.objects.get(id=request.session["userid"]),
        "all_authors": Author.objects.all()
        }
        return render(request, "add-book-review.html", context)

def book_info(request, book_id):
    logged_user = User.objects.get(id=request.session["userid"])
    selected_book = Book.objects.get(id=book_id)

    context = {
        "user_info": User.objects.get(id=request.session["userid"]),
        "book_info": selected_book,
        "all_reviews": Review.objects.filter(book_id=selected_book)
    }        

    return render(request, 'book-info.html', context)

def add_review(request, book_id):
    logged_user = User.objects.get(id=request.session["userid"])

    review = Review.objects.create(
        user_id = logged_user,
        book_id = Book.objects.get(id = book_id),
        review = request.POST["review"],
        rating = request.POST["rating"]
    )

    return redirect(f'/books/{book_id}')

def user_profile(request, user_id):
    selected_user = User.objects.get(id=user_id)

    context = {
        "logged_user": User.objects.get(id=request.session["userid"]),
        "user_info": selected_user,
        "all_books": Book.objects.filter(uploaded_by=selected_user),
        "all_reviews": Review.objects.filter(user_id=selected_user)
    }        

    return render(request, 'user-profile.html', context)

def delete_review(request, review_id):
    review_to_delete = Review.objects.get(id=review_id)
    book_id = review_to_delete.book_id.id
    review_to_delete.delete()
    return redirect(f'/books/{book_id}')