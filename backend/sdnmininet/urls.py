from django.urls import path
from . import views

urlpatterns = [
    path('depth_<int:depth>/fanout_<int:fanout>/', views.process_mininet_parameters, name='mininet_parameters'),
]