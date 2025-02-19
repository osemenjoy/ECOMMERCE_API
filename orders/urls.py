from django.urls import path
from .views import OrderCreateView, OrderListView, OrderDetailsView, OrderUpdateView, OrderCancelView, OrderSearchView

urlpatterns = [
    path("create/", OrderCreateView.as_view(), name="order_create"),
    path("", OrderListView.as_view(), name="order_list"),
    path("<uuid:pk>/", OrderDetailsView.as_view(), name="order_detail"),
    path("<uuid:pk>/edit/", OrderUpdateView.as_view(), name="order_update"),
    path("<uuid:pk>/cancel/", OrderCancelView.as_view(), name="order_cancel"),
    path("search/", OrderSearchView.as_view(), name="order_search"),
]