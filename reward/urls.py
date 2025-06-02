from django.urls import path
from .views import *

urlpatterns = [
    path('create-reward/', CreateCardView.as_view(), name='create-reward'),
    # path('skretch-reward/', CreateReedomView.as_view(), name= 'skretch-reward'),
    path('reedom-reward/', CreateReedomView.as_view(), name= 'reedom-reward'),
]
