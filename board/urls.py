
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('mission_fields/', views.mission_fields, name="mission_fields"),
    path('mission-field/<slug:slug>/', views.mission_fields_detail, name="mission_detail"),
    path('blog/', views.post_list, name="blog"),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name="blog_detail"),
    # path('search_mission/', views.search_mission, name="search_mission"),
    path('donate/', views.initiate_payment, name="initiate_payment"),
    path('<str:ref>/', views.verify_payment, name="verify_payment"), 
]
