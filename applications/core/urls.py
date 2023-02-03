from django.urls import path
from .views import *

urlpatterns = [
    # ******************* Base *******************
    path('', BaseView.as_view(), name='home'),   
]