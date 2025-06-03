from django.urls import path
from .views import *

urlpatterns = [
    path('create-card/', CreateCardView.as_view(), name='create-card'),

    path('scratch-card/', CardScratchView.as_view(), name= 'scratch-card'),

    path('reedom-card/', CardReedomView.as_view(), name= 'reedom-card'),

    path('reedom-coin/', ReedomCoinView.as_view(), name= 'reedom-coin'),
]

