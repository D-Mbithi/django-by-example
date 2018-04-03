from django.shortcuts import render, get_object_or_404
from .models import Post
# Create your views here.


def post_list(request):
    post = Post.publish.all()

    template = 'blog/post/list.html'
    context = {'post': post}

    return render(request, template, context)


def post_details(request, year, month, day, post):
    post = get_object_or_404(Post,
                             slug=post,
                             status=published,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                            )

    template = 'blog/post/detail.html'
    context = {'post': post}

    return render(request, template, context)
