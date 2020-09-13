
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import ( product_list_view ,ProductListView,ProductDetailView,
                            product_detail_view,ProductFeatureView,ProductFeatureDetailView,
                            ProductSlugViewDetail
                           )

urlpatterns = [
    
    path('', ProductListView.as_view(), name="list"),
    path('<slug:slug>/', ProductSlugViewDetail.as_view() , name="detail")
    
] 
