from django.urls import path
from recipes import views as recipes_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    #path('', recipes_views.index, name='home'),
    path('', recipes_views.index.as_view(), name='home'),
    path('api/recipes/', recipes_views.recipe_list),
    path('api/recipes/<int:pk>/', recipes_views.recipe_detail),
    path('api/recipes/published/', recipes_views.recipe_list_published),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#do I need to change anything on this