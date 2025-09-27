from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse

class ProcessPaymentView(TemplateView):
    template_name = 'payments/process.html'

class PaymentSuccessView(TemplateView):
    template_name = 'payments/success.html'

class PaymentCancelView(TemplateView):
    template_name = 'payments/cancel.html'

class PaymentAPIView(TemplateView):
    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'Payments API endpoint'})
