from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('items/', views.ItemListView.as_view(), name='item_list'),
    path('items/create/', views.ItemCreateView.as_view(), name='item_create'),
    path('items/<int:pk>/', views.ItemDetailView.as_view(), name='item_detail'),
    path('items/update/<int:pk>/', views.ItemUpdateView.as_view(), name='item_update'),
    path('items/delete/<int:pk>/', views.ItemDeleteView.as_view(), name='item_delete'),
    path('movement/', views.StockMovementCreateView.as_view(), name='stock_movement'),
    path('report/', views.ReportView.as_view(), name='report'),
    path('export/csv/', views.export_items_csv, name='export_csv'),
    path('low-stock/', views.LowStockView.as_view(), name='low_stock'),
    path('reorder-alerts/', views.ReorderAlertView.as_view(), name='reorder_alert'),
    path('audit-logs/', views.AuditLogView.as_view(), name='audit_log'),
    # Category URLs
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('categories/update/<int:pk>/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('categories/delete/<int:pk>/', views.CategoryDeleteView.as_view(), name='category_delete'),
    # Supplier URLs
    path('suppliers/', views.SupplierListView.as_view(), name='supplier_list'),
    path('suppliers/create/', views.SupplierCreateView.as_view(), name='supplier_create'),
    path('suppliers/update/<int:pk>/', views.SupplierUpdateView.as_view(), name='supplier_update'),
    path('suppliers/delete/<int:pk>/', views.SupplierDeleteView.as_view(), name='supplier_delete'),
    # Item Batch URLs
    path('items/<int:item_id>/batches/', views.ItemBatchListView.as_view(), name='batch_list'),
    path('items/<int:item_id>/batches/create/', views.ItemBatchCreateView.as_view(), name='batch_create'),
    path('batches/<int:pk>/delete/', views.ItemBatchDeleteView.as_view(), name='batch_delete'),
]