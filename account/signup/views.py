from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import CustomLoginForm, SignUpForm, ProfileUpdateForm, TodoItemForm, GuestbookForm, PostForm, CommentForm
from .models import CustomUser, Guestbook, TodoItem, Post, Category, Comment
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.utils import timezone

def firstpage(request):
    return render(request, 'firstpage.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "가입이 성공적으로 완료되었습니다. 로그인 해주세요.")
            return redirect(reverse('firstpage') + '?signup_success=true')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            user = form.authenticate_user()  
            if user is not None:
                login(request, user)
                return redirect('home')  
            else:
                messages.error(request, "로그인 실패. 다시 시도해주세요.")
        else:
            messages.error(request, "로그인 폼에 오류가 있습니다. 다시 확인해주세요.")
    else:
        form = CustomLoginForm()
    return render(request, 'login_view.html', {'form': form})

def home(request):
    return render(request, 'home.html')

def signup_success(request, pk=None):
    if request.user.is_authenticated:  
        user = request.user
        if pk:
            updated_user = CustomUser.objects.get(pk=pk)
            context = {
                'id': updated_user.id,
                'name': updated_user.name,
                'email': updated_user.email,
                'major': updated_user.major,
                'nickname': updated_user.nickname,
                'phone_number':updated_user.phone_number,
                'age':updated_user.age,
                'hobbies':updated_user.hobbies,
                'photo':updated_user.photo,
            }
        else:
            context = {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'major': user.major,
                'nickname': user.nickname,
                'phone_number':user.phone_number,
            }
        return render(request, 'signup_success.html', context)
    else:
        return redirect('login_view') 

def profile_update_view(request):
    if not request.user.is_authenticated:
        return redirect('login_view')  
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            updated_user = CustomUser.objects.get(pk=request.user.pk)
            return redirect('signup_success', pk=updated_user.pk) 
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'profile_update.html', {'form': form})

def guestbook_list(request):
    guestbook_messages = Guestbook.objects.all().order_by('-created_at')
    return render(request, 'guestbook_list.html', {'messages': guestbook_messages})

def add_message(request):
    if request.method == "POST":
        form = GuestbookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('guestbook_list')
    else:
        form = GuestbookForm()
    return render(request, 'add_message.html', {'form': form})

def todo_list(request):
    if not request.user.is_authenticated:
        return redirect('login_view')
    todo_items = TodoItem.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'todo_list.html', {'todo_items': todo_items})

def add_todo_item(request):
    if not request.user.is_authenticated:
        return redirect('login_view')
    if request.method == "POST":
        form = TodoItemForm(request.POST)
        if form.is_valid():
            todo_item = form.save(commit=False)
            todo_item.user = request.user
            todo_item.save()
            return redirect('todo_list')
    else:
        form = TodoItemForm()
    return render(request, 'add_todo_item.html', {'form': form})

def toggle_todo_item_completed(request, item_id):
    if not request.user.is_authenticated:
        return redirect('login_view')
    todo_item = get_object_or_404(TodoItem, id=item_id)
    if request.user == todo_item.user:
        todo_item.completed = not todo_item.completed
        if todo_item.completed:
            todo_item.completed_at = timezone.now()
        else:
            todo_item.completed_at = None
        todo_item.save()
    return redirect('todo_list')


def edit_todo_item(request, id):
    todo_item = get_object_or_404(TodoItem, id=id)

    if request.method == 'POST':
        form = TodoItemForm(request.POST, instance=todo_item)
        if form.is_valid():
            form.save()
            return redirect('todo_list')
    else:
        form = TodoItemForm(instance=todo_item)
    
    return render(request, 'edit_todo_item.html', {'form': form})


def delete_todo_item(request, id):
    if not request.user.is_authenticated:
        return redirect('login_view')
    todo_item = get_object_or_404(TodoItem, id=id)
    if request.user == todo_item.user:
        todo_item.delete()
    return redirect('todo_list')


def post_list(request, category_id=None):
    categories = Category.objects.all()
    if category_id:
        posts = Post.objects.filter(category_id=category_id).order_by('-created_at')
        selected_category = get_object_or_404(Category, id=category_id)
    else:
        posts = Post.objects.all().order_by('-created_at')
        selected_category = None
    return render(request, 'post_list.html', {'posts': posts, 'categories': categories, 'selected_category': selected_category})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        comment_form = CommentForm()
    return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})



def add_post(request):
    if not request.user.is_authenticated:
        return redirect('login_view')
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  # 현재 로그인된 사용자 설정
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'add_post.html', {'form': form})



def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
    
    return render(request, 'edit_post.html', {'form': form, 'post': post})


def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    
    return render(request, 'delete_post.html', {'post': post})
