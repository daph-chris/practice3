from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.index, name='index'),              # /
    path('index.html', views.index, name='index_html'),  # /index.html
    path('run-tests/', views.run_tests, name='run_tests'),
    path('download-report/', views.download_report, name='download_report'),
]
