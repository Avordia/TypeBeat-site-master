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
    path('mybeatpack/<str:name>/', views.upload_beatpack, name='upload_beatpack'),
    path('mybeatpack/<str:name>/<int:id>/<str:beatpack_title>', views.my_beatmap, name='my_beatmap'),
    path('beatmap_leaderboard/<int:beatmap_id>/', views.beatmap_leaderboard ,name='beatmap_leaderboard'),
    path('download_beatpack/<int:beatpack_id>/', views.download_beatpack, name='download_beatpack'),
    path('user/', views.user_page, name='user_page'),
    path('user/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('user/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('play/<int:beatmap_id>/', views.play, name='play'),
    path('beatpacks/', views.viewAllBeatmap, name="beatpacks"),
    path('update/<str:model_name>/<int:obj_id>/', views.update_field, name='update_field'),
    path('delete/<str:model_name>/<int:obj_id>/', views.delete_item, name='delete_item'),
    path('beatpack/<int:beatpack_id>/', views.beatpack_detail, name='beatpack_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
