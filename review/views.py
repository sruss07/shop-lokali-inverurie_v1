from django.shortcuts import render, get_object_or_404, redirect
from .models import Review
from .forms import ReviewForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def review_list(request):
    reviews = Review.objects.all()
    return render(request, 'review/review.html', {'reviews': reviews})


def review_detail(request, pk):
    review = get_object_or_404(Review, pk=pk)
    return render(request, 'review/review_details.html', {'review': review})


@login_required
def review_new(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.published_date = timezone.now()
            review.save()
            return redirect('review_detail', pk=review.pk)
    else:
        form = ReviewForm()
    return render(request, 'review/review_add.html', {'form': form})


@login_required
def review_edit(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.published_date = timezone.now()
            review.save()
            return redirect('review_detail', pk=review.pk)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'review/review_edit.html', {'form': form})


@login_required
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    review.delete()
    return redirect('review_list')

