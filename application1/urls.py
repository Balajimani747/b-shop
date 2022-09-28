from django.urls import path
from .import views

urlpatterns = [   
path('',views.Home,name="home_page"),
path('register/',views.Register,name="register_page"),
path('login/',views.Login,name="login_page"),
path('log_out/',views.Log_out,name="logout_page"),
path('collections/',views.Collections,name="collection_page"),
path('collections/<str:name>',views.Collections_view,name="collection_page2"),
path('collections/<str:cname>/<str:pname>',views.Product_details,name="productdetails_page2"),
path('addtocart',views.Add_to_cart,name="cart_page"),
path('addtocart1',views.Cart_page,name="cart_page1"),
]
 