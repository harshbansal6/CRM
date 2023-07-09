from django.urls import path

from . import views

urlpatterns = [
    path('add-lead/', views.add_lead, name='add_lead'),
    path('<int:pk>/', views.lead_details, name='leads_detail'),
    path('', views.leads_list, name='leads_list'),
]