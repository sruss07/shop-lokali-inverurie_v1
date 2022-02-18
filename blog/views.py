from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog
from .forms import BlogForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def blog_list(request):
    blogs = Blog.objects.all()
    return render(request, 'blog/blog.html', {'blogs': blogs})


def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    return render(request, 'blog/blog_details.html', {'blog': blog})


@login_required
def blog_new(request):
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.published_date = timezone.now()
            blog.save()
            return redirect('blog_detail', pk=blog.pk)
    else:
        form = BlogForm()
    return render(request, 'blog/blog_add.html', {'form': form})


@login_required
def blog_edit(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == "POST":
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.published_date = timezone.now()
            blog.save()
            return redirect('blog_detail', pk=blog.pk)
    else:
        form = BlogForm(instance=blog)
    return render(request, 'blog/blog_edit.html', {'form': form})


@login_required
def blog_delete(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    blog.delete()
    return redirect('blog_list')
