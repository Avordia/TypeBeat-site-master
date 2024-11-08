from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from TypeBeat import views

urlpatterns = [
    path('', views.login_view, name='login'), 
    path('homepage/<str:name>/', views.homepage, name='homepage'),  
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('AdminPage/', views.AdminPage, name='AdminPage'),

    path('update/<str:model_name>/<int:obj_id>/', views.update_field, name='update_field'),
    path('delete/<str:model_name>/<int:obj_id>/', views.delete_item, name='delete_item'),
]
