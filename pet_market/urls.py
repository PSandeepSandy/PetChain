from django.conf.urls import url
from django.urls import path

from pet_market import views


urlpatterns = [
    url(r'^$', views.home, name='Home Page'),
    url(r'^items/(?P<item_id>[-\w]+)$', views.display_item, name='display_item'),
    path('seller/post-ad', views.post_ad, name="Post Ad"),
    path('seller/post-ad/get-item-attr/', views.get_attributes),
    path('seller/post-ad/get-invalid-fields/', views.get_invalid_fields),
    path('seller/my-sales/', views.mysales),
]