from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from TypeBeat import views

urlpatterns = [
    path('', views.login_view, name='login'), 
    path('homepage/<str:name>/', views.homepage, name='homepage'),  
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
