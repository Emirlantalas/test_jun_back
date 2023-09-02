from django.urls import path
from . import views



urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('cards/', views.CardListView.as_view(), name='card-list'),
    path('purchases/', views.PurchaseListView.as_view(), name='purchase-list'),
    path('cards/<int:card_id>/purchases/', views.PurchaseHistoryView.as_view(), name='purchase-history'),
    path('purchases/delete/', views.PurchaseDeleteView.as_view(), name='purchase-delete'),
    path('cards/<int:card_id>/activate/', views.CardActivationView.as_view(), name='card-activate'),
    path('cards/<int:card_id>/deactivate/', views.CardDeactivationView.as_view(), name='card-deactivate'),
    path('cards/<int:card_id>/delete/', views.CardDeleteView.as_view(), name='card-delete-confirm'),
    path('cards/<int:card_id>/delete/confirmed/', views.CardDeleteConfirmedView.as_view(), name='card-delete'),
    path('card_list/', views.CardListView.as_view(), name='card-list-view'),
    path('cards/create/', views.create_card, name='create-card'),
    path('api/cards/', views.CardListAPIView.as_view(), name='card-list-api'),
    path('api/purchases/', views.PurchaseListAPIView.as_view(), name='purchase-list-api'),
    path('purchase-filter/', views.purchase_filter, name='purchase-filter'),
]

