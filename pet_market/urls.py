from django.conf.urls import url
from django.urls import path

from pet_market import views


urlpatterns = [
    url(r'^$', views.home, name='home_page'),
    url(r'^items/(?P<item_id>[-\w]+)$', views.display_item, name='display_item'),
    path('seller/post-ad', views.post_ad, name="Post Ad"),
    path('seller/post-ad/get-item-attr/', views.get_attributes),
    path('seller/post-ad/get-invalid-fields/', views.get_invalid_fields),
    path('seller/my-sales/', views.mysales),
    path('filters/', views.apply_filters),
    path('buyer/my-cart/', views.my_cart),
    path('buyer/add-to-cart', views.add_to_cart),
]