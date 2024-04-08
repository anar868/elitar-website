from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login', views.user_login, name='login'),
    path('add-missing', views.add_missing, name='add_missing'),
    path('logout', views.user_logout, name='logout'),
    path('remove_missing', views.remove_missing, name='remove_missing'),
    path('class_checked', views.class_checked, name='class_checked'),
    path('class_list', views.class_list, name='class_list'),
    path('missing_students/<int:class_id>', views.missing_students, name='missing_students'),
    path('add_user', views.add_user, name='add_user')
]