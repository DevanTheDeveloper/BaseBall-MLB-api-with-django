from django.urls import path,include
from . import views
from dashboard.dash_apps.finished_apps import example
from django.conf.urls.static import static
import core.settings as settings


urlpatterns = [
	path('mlb/', views.index, name="index"),
	path('mlb/team/<int:teamID>/', views.rosterView, name='roster'),
	path('mlb/team/<int:teamID>/player/<int:playerID>/', views.playerView, name='player_profile'),
	path('mlb/team_stats/',views.team_stats,name='team_stats'),
	path('mlb/team_salaries/',views.team_salaries,name='team_salaries'),
	path('mlb/upload_file', views.upload_file, name='upload_file'),
	path('mlb/download_file', views.download_file, name='download_file'),
	
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)