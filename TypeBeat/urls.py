from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from TypeBeat import views
from TypeBeat.views import delete_item

urlpatterns = [
    path('', views.login_view, name='login'), 
    path('homepage/<str:name>/', views.homepage, name='homepage'),  
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('AdminPage/', views.AdminPage, name='AdminPage'),
    path('logout/', views.logout_view, name='logout'),
    path('BeatPack_Upload/<str:name>/', views.BeatPack_Upload, name='BeatPack_Upload'),
    path('beatmap_leaderboard/<int:beatmap_id>/', views.beatmap_leaderboard, name='beatmap_leaderboard'),


    path('update/<str:model_name>/<int:obj_id>/', views.update_field, name='update_field'),
    path('delete/<str:model_name>/<int:obj_id>/', delete_item, name='delete_item'),
    path('beatpack/<int:beatpack_id>/', views.beatpack_detail, name='beatpack_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
