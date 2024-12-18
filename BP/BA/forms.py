from django import forms
from .models import CustomUser
class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('last_name', 'first_name', 'middle_name', 'username', 'email', 'password1', 'password2', 'avatar', 'bio')



from django.contrib.auth.forms import AuthenticationForm
class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('last_name', 'first_name', 'middle_name', 'username', 'avatar', 'bio')



from .models import Post
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']



from .models import Comment
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']