from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (
    firstpage, signup, signup_success, login_view, home, profile_update_view,
    todo_list, add_todo_item, toggle_todo_item_completed, post_list, post_detail, add_post,
    edit_post, delete_post
)
from . import views

urlpatterns = [
    path('', firstpage, name='firstpage'),
    path('signup/', signup, name='signup'),
    path('signup/signup_success/<str:pk>', signup_success, name='signup_success'),
    path('login_view/', login_view, name='login_view'),
    path('home/', home, name='home'),
    path('profile/update/', profile_update_view, name='profile_update'),
    path('guestbook/', views.guestbook_list, name='guestbook_list'),
    path('guestbook/add/', views.add_message, name='add_message'),
    path('todo/', todo_list, name='todo_list'),
    path('todo/add/', add_todo_item, name='add_todo_item'),
    path('todo/toggle_completed/<int:item_id>/', toggle_todo_item_completed, name='toggle_todo_item_completed'),
    path('todo/delete/<int:id>/', views.delete_todo_item, name='delete_todo_item'),
    path('todo/edit/<int:id>/', views.edit_todo_item, name='edit_todo_item'),
    path('posts/', post_list, name='post_list'),
    path('posts/category/<int:category_id>/', post_list, name='post_list_by_category'),
    path('posts/<int:post_id>/', post_detail, name='post_detail'),
    path('posts/add/', add_post, name='add_post'),
    path('posts/edit/<int:post_id>/', edit_post, name='edit_post'),
    path('posts/delete/<int:post_id>/', delete_post, name='delete_post'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
