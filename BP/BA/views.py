def index(request):
    return render(request,'index.html')


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



def profile_view(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})



def delete_profile_view(request):
    if request.method == 'POST':

        user = request.user

        # Удаление всеч постов и комментариев пользователя:
        # Post.objects.filter(author=user).delete()
        # Comment.objects.filter(author=user).delete()

        user.delete()

        return redirect('BA:index')

    return render(request, 'confirm_delete.html')



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



from django.contrib.auth import login, authenticate, logout
def logout_user(request):
    logout(request)
    return render(request,'registration/logged_out.html')