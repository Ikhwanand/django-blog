from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Categories
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    categories = Categories.objects.all()
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    latest_post = Post.objects.order_by('-created_at')[0]

    # Filter posts by search query if provided
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |  # Search for query in title
            Q(content__icontains=query)  # or in content
        )

    # Filter posts by category if category_id is provided
    if category_id:
        posts = posts.filter(category_id=category_id)
        
    # Paginate posts
    paginator = Paginator(posts, 4) # show 2 posts per page
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    # Render the post list template with filtered posts and all categories
    return render(request, 'blog/post_list.html', {
        'posts': posts,
        'categories': categories,
        'latest_post': latest_post,
    })
    
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {
        'post': post
    })
    

@login_required
def post_create(request):
    # If the request is a POST, process the form
    if request.method == 'POST':
        # Create a PostForm instance with the request data
        form = PostForm(request.POST, request.FILES)
        # If the form is valid, save the post
        if form.is_valid():
            # Save the post but don't commit it to the database yet
            post = form.save(commit=False)
            # Set the author of the post to the current user
            post.author = request.user
            # Save the post to the database
            post.save()
            # Redirect to the post detail page
            return redirect('blog:post_detail', pk=post.pk)
    else:
        # If the request is a GET, create a blank PostForm instance
        form = PostForm()
    # Render the post form template with the form
    return render(request, 'blog/post_form.html', {
        'form': form
    })
    
    
@login_required
def post_edit(request, pk):
    # Get the post object from the database
    post = get_object_or_404(Post, pk=pk)
    # If the request is a POST, process the form
    if request.method == 'POST':
        # Create a PostForm instance with the request data and the current post object
        form = PostForm(request.POST, request.FILES, instance=post)
        # If the form is valid, update the post object in the database
        if form.is_valid():
            # Save the post object but don't commit it to the database yet
            post = form.save(commit=False)
            # Set the author of the post to the current user
            post.author = request.user
            # Save the post object to the database
            post.save()
            # Redirect to the post detail page
            return redirect('blog:post_detail', pk=post.pk)
    else:
        # If the request is a GET, create a PostForm instance with the current post object
        form = PostForm(instance=post)
    # Render the post form template with the form
    return render(request, 'blog/post_form.html', {
        'form': form
    })

    
    
    
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('blog:post_list')