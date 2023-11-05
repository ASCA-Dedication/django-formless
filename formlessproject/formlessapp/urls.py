from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("customemodel", views.customemodel, name="customemodel"),

    # path("about/", views.about, name="AboutUs"),
    # path("contact/", views.contact, name="ContactUs"),
    # path("products/<int:myid>", views.productView, name="ProductView"),
    # path("products/<str:myslug>", views.productView, name="ProductView"),

# Actions

    path('chat/', views.chat_view, name='chat_view'),


]