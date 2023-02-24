from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import redirect
from django.core.paginator import Paginator
from .models import ImagePost, Follow, Like
from .forms import ImageForm
User = get_user_model()


def index(request):
    image_list = ImagePost.objects.all()
    paginator = Paginator(image_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    print(context)
    return render(request, 'img/index.html', context)


@login_required
def img_create(request):
    form = ImageForm(
        request.POST or None,
        files=request.FILES or None,
    )
    author_user = request.user.username
    if request.method == 'POST' and form.is_valid():
        img = form.save(commit=False)
        img.author = request.user
        img.save()
        return redirect(reverse(
            'img:profile', kwargs={'username': f'{author_user}'})
        )
    context = {'form': form}
    return render(request, 'img/img_create.html', context)


def img_detail(request, img_id):
    img = get_object_or_404(ImagePost, pk=img_id)
    user = request.user
    username = img.author
    number_posts = username.images.count()
    likes = img.likes.count()
    context = {
        'img': img,
        'number_posts': number_posts,
        'user': user,
        'username': username,
        'likes': likes,
        
    }
    return render(request, 'img/img_detail.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    number_posts = author.images.count()
    post_list = author.images.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    author_follow = get_object_or_404(User, username=username)
    follow = None
    if request.user.is_authenticated:
        follow_exist = Follow.objects.filter(
            author=author_follow, user=request.user
        ).exists()
        if follow_exist:
            follow = 'following'
        else:
            follow = None
    context = {
        'page_obj': page_obj,
        'number_posts': number_posts,
        'author': author,
        'following': follow
    }
    return render(request, 'img/profile.html', context)

@login_required
def follow_index(request):
    # информация о текущем пользователе доступна в переменной request.user
    posts = ImagePost.objects.filter(author__following__user=request.user)
    paginator = Paginator(posts, 10)

    # Из URL извлекаем номер запрошенной страницы - это значение параметра page
    page_number = request.GET.get('page')

    # Получаем набор записей для страницы с запрошенным номером
    page_obj = paginator.get_page(page_number)
    # Отдаем в словаре контекста
    context = {
        'page_obj': page_obj,
    }

    return render(request, 'img/follow.html', context)


@login_required
def profile_follow(request, username):
    # Подписаться на автора

    author_follow = get_object_or_404(User, username=username)
    if author_follow != request.user:
        Follow.objects.get_or_create(
            user=request.user,
            author=author_follow
        )
    return redirect('img:profile', username=username)


@login_required
def profile_unfollow(request, username):
    # Дизлайк, отписка
    follow = Follow.objects.filter(
        author__username=username, user=request.user
    )
    follow.delete()
    return redirect('img:profile', username=username)


@login_required
def img_like(request, img_id):
    image = get_object_or_404(ImagePost, pk=img_id)
    Like.objects.get_or_create(
        image=image,
        author=request.user
    )
    return redirect('img:index')
