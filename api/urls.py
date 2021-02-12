from django.urls import path
from rest_framework.authtoken import views
from api.views import *

urlpatterns = [
    # Main rule condition
    path('testViewApi/records',
         testViewApi.as_view({'post': 'records'})),
    path('testViewApi/create',
         testViewApi.as_view({'post': 'create'})),
    path('testViewApi/<str:id>',
         testViewApi.as_view({'get': 'record'})),
    path('testViewApi/<str:id>/update',
         testViewApi.as_view({'post': 'update'})),
    path('testViewApi/<str:id>/delete',
         testViewApi.as_view({'delete': 'delete'})),
]
