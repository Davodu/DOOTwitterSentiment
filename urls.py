from django.conf.urls import url
import views 

urlpatterns = [
	url(r'^bp[?Pphrase_state\w{1,50}=+-]*',views.background_process, name = 'bp'),
	url(r'^$',views.index, name='index'),
	url(r'^results.html/', views.results, name = 'results'),
]