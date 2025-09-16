from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Movie, Review


def index(request):
    """
    Show only movies that are available:
      - amount_left is NULL (unlimited), OR
      - amount_left > 0
    Still supports your ?search= query param.
    """
    search_term = request.GET.get('search', '').strip()

    base_qs = Movie.objects.filter(
        Q(amount_left__isnull=True) | Q(amount_left__gt=0)
    )

    if search_term:
        movies = base_qs.filter(
            Q(name__icontains=search_term) | Q(description__icontains=search_term)
        )
    else:
        movies = base_qs

    template_data = {
        'title': 'Movies',
        'movies': movies,
        'search': search_term,
    }
    return render(request, 'movies/index.html', {'template_data': template_data})


def show(request, id):
    movie = get_object_or_404(Movie, id=id)
    reviews = Review.objects.filter(movie=movie)

    template_data = {
        'title': movie.name,
        'movie': movie,
        'reviews': reviews,
    }
    return render(request, 'movies/show.html', {'template_data': template_data})


@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST.get('comment', '').strip():
        movie = get_object_or_404(Movie, id=id)
        review = Review(comment=request.POST['comment'], movie=movie, user=request.user)
        review.save()
        return redirect('movies.show', id=id)
    return redirect('movies.show', id=id)


@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)

    if request.method == 'GET':
        template_data = {
            'title': 'Edit Review',
            'review': review,
        }
        return render(request, 'movies/edit_review.html', {'template_data': template_data})

    elif request.method == 'POST' and request.POST.get('comment', '').strip():
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)

    return redirect('movies.show', id=id)


@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('movies.show', id=id)


# -------- NEW: purchase endpoint (decrease stock by 1) --------
@login_required
def purchase_one(request, id):
    """
    Decrease amount_left by 1 if there is stock or it's unlimited.
    Redirect back to the movie detail either way.
    """
    movie = get_object_or_404(Movie, id=id)

    # Unlimited (NULL) or > 0 -> allow purchase
    if movie.amount_left is None or movie.amount_left > 0:
        # model helper handles clamping at 0 and saving
        try:
            movie.decrease_amount(1)
            messages.success(request, f"Purchased 1 copy of '{movie.name}'.")
        except Exception:
            # fallback if helper not present for any reason
            if movie.amount_left is not None and movie.amount_left > 0:
                movie.amount_left = max(0, movie.amount_left - 1)
                movie.save(update_fields=['amount_left'])
                messages.success(request, f"Purchased 1 copy of '{movie.name}'.")
    else:
        messages.error(request, f"'{movie.name}' is sold out.")

    return redirect('movies.show', id=id)
