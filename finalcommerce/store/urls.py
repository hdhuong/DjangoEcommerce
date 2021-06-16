from django.urls import path

from . import views

urlpatterns = [
        #Leave as empty string for base url
    path('index',views.index,name="index"),
    path('',views.index2,name="index2"),
	path('store/', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
    path('login/',views.loginPage,name="login"),
    path('logout/',views.logoutUser,name="logout"),
    path('register/',views.registerPage,name="register"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('staffhome/', views.staffHome, name="staffhome"),
    path('details/<int:id>/', views.detailPage, name="details"),
    
]