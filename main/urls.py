from django.urls import path
from . import views  # imports views from the same app


urlpatterns = [
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('chatbot/', views.chatbot_view, name='chatbot'),
    path('recommendation/', views.recommender_view, name='recommender'),
    path("life-advice/", views.life_advice_view, name="life_advice"),

]