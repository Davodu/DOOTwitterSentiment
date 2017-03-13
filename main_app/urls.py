from django.conf.urls import url
from main_app import views


urlpatterns = [
	url(r'^$', views.index, name = "index"),
	url(r'^home/', views.home, name = "home"),
	url(r'^get_raw_tweets/',views.raw_tweets, name = "raw_tweets"),
]