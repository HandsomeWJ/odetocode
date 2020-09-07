from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('guide.html', views.guide, name="guide"),
    path('risk.html', views.risk, name="risk"),
    path('success.html', views.success, name="success"),
    path('news.html', views.news, name="news"),
    
]
