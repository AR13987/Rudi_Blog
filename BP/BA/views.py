# Главная страница:
from django.core.paginator import Paginator
from .models import Post
def index(request):
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 50)  # 50 постов на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'index.html', {'page_obj': page_obj})



# Редактирование профиля:
from .forms import UserProfileForm
from django.contrib.auth.decorators import login_required
@login_required
def editing_profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('BA:profile')
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'editing_profile.html', {'form': form})



# Профиль:
def profile_view(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})



# Удаление профиля:
from .models import Comment
def delete_profile_view(request):
    if request.method == 'POST':

        user = request.user

        # Удаление всеч постов и комментариев пользователя:
        Post.objects.filter(author=user).delete()
        Comment.objects.filter(author=user).delete()

        user.delete()

        return redirect('BA:index')

    return render(request, 'confirm_delete.html')



# Создание поста:
from .forms import PostForm
def create_post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('BA:index')  # Перенаправление на главную страницу
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})



# Лайк:
def like_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('BA:index')



# Мои посты:
def my_posts(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, 'my_posts.html', {'posts': posts})



# Редактирование поста:
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        return redirect('BA:index')

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('BA:my_posts')
    else:
        form = PostForm(instance=post)

    return render(request, 'edit_post.html', {'form': form, 'post': post})


# Удаление поста:
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        return redirect('BA:index')

    if request.method == 'POST':
        post.delete()
        return redirect('BA:index')

    return render(request, 'delete_post.html', {'post': post})



#Регистрация:
from django.shortcuts import redirect, render, get_object_or_404
from .forms import CustomUserCreationForm, CustomAuthenticationForm
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # Хранение пароля в зашифрованном виде
            user.save()
            login(request, user)  # Автоматический вход после регистрации
            return redirect('BA:index')
        else:
            print(form.errors)  # Вывод ошибок формы для отладки
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})



# Авторизация:
def login_user(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('BA:index')
            else:
                form.add_error(None, 'Неверный логин или пароль.')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})



# Выход:
from django.contrib.auth import login, authenticate, logout
def logout_user(request):
    logout(request)
    return render(request,'registration/logged_out.html')