"""from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls.static import static
from django.conf import settings"""



"""urlpatterns = [
    path('register/', user_views.register, name='register'),
    path('login/',
         auth_views.LoginView.as_view(template_name='users/login.html'),
         name='login'),
    path('logout/',
         auth_views.LogoutView.as_view(template_name='users/logout.html'),
         name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)"""

from django.urls import path
from users import views as users_views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    #path('', users_views.index, name='home'),
    path('login/', users_views.login.as_view(), name='login'),
    path('logout/', users_views.logout.as_view(), name='logout'),
    path('register/', users_views.register.as_view(), name='register'),
    path('api/users/', users_views.username),
    path('api/users/<int:pk>/', users_views.user_detail),
    path('api/users/published/', users_views.user_list_published),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#do I need to change anything on this