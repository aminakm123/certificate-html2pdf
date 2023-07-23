from django.contrib import admin
from django.urls import path,include
from pdfcertificate import views

urlpatterns = [
    path('',views.create_certificate,name='create_certificate'),
    path('pdf-certificate/<str:pk>/',views.pdf_certificate,name='pdf_certificate'),
    path('verify-certificate/',views.verify_certificate,name='verify_certificate')
] 
