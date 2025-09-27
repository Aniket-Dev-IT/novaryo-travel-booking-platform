from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('process/', views.ProcessPaymentView.as_view(), name='process'),
    path('success/', views.PaymentSuccessView.as_view(), name='success'),
    path('cancel/', views.PaymentCancelView.as_view(), name='cancel'),
    path('api/payment/', views.PaymentAPIView.as_view(), name='payment_api'),
]