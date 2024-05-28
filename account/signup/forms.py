from django import forms
from django.core.exceptions import ValidationError
from .models import CustomUser, Guestbook, TodoItem, Post, Category, Comment
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

class SignUpForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields=('id','name','email','major','nickname','password','phone_number')
        widgets = {'password': forms.PasswordInput()}
    
    def clean_id(self):
        user_id = self.cleaned_data.get('id')
        if CustomUser.objects.filter(id=user_id).exists():
            raise ValidationError('이미 사용 중인 ID입니다. 다른 ID를 선택해주세요.')
        return user_id

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
    
class CustomLoginForm(forms.Form):
    id = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ID'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'PW'}))
    
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)

    def authenticate_user(self):
        user_id = self.cleaned_data.get('id')
        password = self.cleaned_data.get('password')
        return authenticate(request=None, id=user_id, password=password)

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['age', 'hobbies', 'photo', 'major', 'nickname','phone_number']
        widgets = {
            'photo': forms.FileInput()
        }

class GuestbookForm(forms.ModelForm):
    class Meta:
        model = Guestbook
        fields = ['name', 'message']


class TodoItemForm(forms.ModelForm):
    class Meta:
        model = TodoItem
        fields = ['title']

    def __init__(self, *args, **kwargs):
        super(TodoItemForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '댓글을 입력하세요...'}),
        }