from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='dashboard-index'),
    path('staff_view/', views.staff_view, name='dashboard-staff'),
    path('product/', views.product, name='dashboard-product'),
    path('products/edit/<int:product_id>/', views.edit_product_view, name='edit-product'),
    path('products/delete/<int:product_id>/', views.delete_product_view, name='delete-product'),
    path('order/', views.order, name='dashboard-order'),
    path('reports/', views.reports_view, name='dashboard-reports'),
    path('reports/download/<str:report_type>/', views.download_report, name='download-report'),
    
]