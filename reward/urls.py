from django.urls import path
from .views import CreateRewardView

urlpatterns = [
    path('create-reward/', CreateRewardView.as_view(), name='create-reward'),
]
