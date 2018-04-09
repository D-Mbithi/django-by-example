from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Post
from django.views.generic import ListView
from .forms import EmailPostForm, PostCreateForm
from django.http import HttpResponseRedirect
# Create your views here.


def index(request):
    return render(request, 'index.html', {})


def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    template = 'blog/post/list.html'
    context = {
                'page': page,
                'posts': posts
                }

    return render(request, template, context)


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                            )

    template = 'blog/post/detail.html'
    context = {'post': post}

    return render(request, template, context)


def post_create(request):
    if request.method == 'POST':
        form = PostCreateForm()

        if form.is_valid:
            form.save()
        return HttpResponseRedirect('/blog/')
    else:
        form = PostCreateForm()

    template = 'blog/post/create.html'
    context = {'form': form}

    return render(request, template, context)


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_url(post.get_absolute_url)
            subject = '{} ({}) recommends reading "{}"'.format(cd['name'], cd['email'], post_url)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.titl, post_url, cd['name'])
            sent=True
    else:
        form = EmailPostForm()

    template = 'blog/post/share.html'
    context = {'form': form}

    return render(request, template, context)
