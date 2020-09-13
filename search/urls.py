
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import SearchListView

urlpatterns = [
    
    path('', SearchListView.as_view(), name="query")
    
]