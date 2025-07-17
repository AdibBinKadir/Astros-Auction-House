from django.urls import path
from . import views

urlpatterns = [
    path('<int:index>', views.prod_red),
    path('<int:index>/<int:scr>', views.products),
    path('left/<int:index>', views.left_prod),
    path('right/<int:index>', views.right_prod),
    path('bid/<int:index>/<int:amount>', views.bid),
    path('get_bids/<int:product_id>/', views.get_info, name='get_bids'),
]