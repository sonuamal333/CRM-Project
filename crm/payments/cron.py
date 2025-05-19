from . models import Payment

from django.utils import timezone

import threading

from student. utility import email_sending

# cron to sent remainder email about payment

def remainder_email():

    current_date = timezone.now().date()

    five_days_before_date =current_date - timezone.timedelta(days = 5)

    pending_payments = Payment.objects.filter(status='Pending',student__Join_date__lte = five_days_before_date)

    if pending_payments.exists():

        for payment in pending_payments:

                subject = 'Login Credentials'

                #sender = settings.EMAIL_HOST_USER 

                recepients = [payment.student.email]

                template = 'email/payment-remainder.html'

                context = {'name':f'{payment.student.first_name} {payment.student.second_name}'}

                #email_sending(subject,recepients,template,context)

                thread =threading.Thread(target=email_sending,args=(subject,recepients,template,context))

                thread.start()

    