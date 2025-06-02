from django.contrib import admin
from django.urls import path
from reward.views import CreateRewardView  # Import your views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', home_view),  # This handles root URL
    path('create-reward/', CreateRewardView.as_view(), name='create-reward'),
]
