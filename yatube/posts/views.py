from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import get_user_model
from .models import Group, Post, Comment, Follow
from .forms import PostForm, CommentForm
from .utils import paginate_page


User = get_user_model()


def index(request):
    template = 'posts/index.html'
    posts = Post.objects.all()
    page_obj = paginate_page(posts, request)
    context = {
        'page_obj': page_obj,
    }
    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.select_related('group', 'author').all()
    page_obj = paginate_page(posts, request)
    template = 'posts/group_list.html'
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.posts.all()
    page_obj = paginate_page(post_list, request)
    template = 'posts/profile.html'
    context = {
        "author": author,
        "post_list": post_list,
        "page_obj": page_obj,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post_count = post.author.posts.count()
    form = CommentForm(request.POST or None)
    comments = Comment.objects.filter(post=post)
    template = 'posts/post_detail.html'
    context = {
        'post': post,
        'post_count': post_count,
        'form': form,
        'comments': comments,
    }
    return render(request, template, context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect("posts:profile", username=request.user)
    template = "posts/create_post.html"
    context = {
        "form": form
    }
    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    is_edit = True
    post = get_object_or_404(Post, pk=post_id)
    form = PostForm(request.POST or None,
                    files=request.FILES or None,
                    instance=post)
    if post.author != request.user:
        return redirect("posts:post_detail", post_id)
    if form.is_valid():
        form.save()
        return redirect("posts:post_detail", post_id)
    template = "posts/create_post.html"
    context = {
        "form": form,
        "is_edit": is_edit,
    }
    return render(request, template, context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    follower = Follow.objects.filter(user=request.user).values_list(
        'author_id', flat=True
    )
    posts = Post.objects.filter(author_id__in=follower)
    page_obj = paginate_page(posts, request)
    template = 'posts/follow.html'
    context = {
        'page_obj': page_obj,
        'title': 'Избранные посты',
    }
    return render(request, template, context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if author != request.user:
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect('posts:follow_index')


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    Follow.objects.get(user=request.user, author=author).delete()
    return redirect('posts:follow_index')
