
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include

urlpatterns = [
	url(r'^main_app/', include("main_app.urls")),
    url(r'^admin/', admin.site.urls),
]
