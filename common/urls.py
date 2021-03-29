from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'common'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('find/', views.find, name='find'),
    path('send/', views.send, name='send'),
    path('change/<int:user_id>', views.change, name='change'),
    path('profile/<int:user_id>', views.profile, name='profile'),
]
