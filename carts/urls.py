from django.urls import path
from .views import (
    AddCartView, 
    CartListView, 
    CartClearView,
    RemoveCartItemView, 
    ClearSessionCart,
    RemoveSessionCartItem,
    EditCartItemView,
    EditCartItemSesion,
    )

urlpatterns = [
    path("add/", AddCartView.as_view(), name="add_cart"),
    path("", CartListView.as_view(), name="list_cart"),
    path("<uuid:pk>/clear/", CartClearView.as_view(), name="clear_cart"),
    path("session-clear/", ClearSessionCart.as_view(), name="clear_session_cart"),
    path("item/<uuid:pk>/remove/", RemoveCartItemView.as_view(), name="remove_item"),
    path("item/<uuid:pk>/edit/", EditCartItemView.as_view(), name="edit_item"),
    path("item/<uuid:product_id>/update/", EditCartItemSesion.as_view(), name="edit_session_item"),
    path("item/<uuid:product_id>/delete/", RemoveSessionCartItem.as_view(), name="remove_session_item"),


]