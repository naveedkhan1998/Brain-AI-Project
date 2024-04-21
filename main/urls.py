from django.urls import path
from .views import home, video_page, video_feed,about_us, contact

urlpatterns = [
    path('', home, name='home'),
    path('video/', video_page, name='video_page'),
    path('video_feed/', video_feed, name='video_feed'),
    path('about-us/', about_us, name='about_us'),
    path('contact/', contact, name='contact'),
]
