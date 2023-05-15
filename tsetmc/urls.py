from django.urls import path, include
from .views import url, api, api2, home1 ,surl, sapi,shome1

urlpatterns = [
    path("url/<str:stock>", url, name='url'),
    path("api", api, name='api'),
    path("api2", api2, name='api2'),
    path("", home1, name='home1'),
    
    path("surl/<str:stock>", surl, name='surl'),
    path("sapi", sapi, name='sapi'),
    path("s", shome1, name='shome1'),

]
