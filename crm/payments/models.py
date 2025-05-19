from django.db import models

from student.models import Baseclass

class PaymentStatusChoices(models.TextChoices):

    PENDING = 'Pending','Pending'

    SUCCESS = 'Success','Success'

    FAILED = 'Failed','Failed'

class Payment(Baseclass):

    student = models.OneToOneField('student.students',on_delete=models.CASCADE)

    amount = models.FloatField()

    status = models.CharField(max_length=20,choices=PaymentStatusChoices.choices,default=PaymentStatusChoices.PENDING)

    paid_at = models.DateTimeField(null=True,blank=True)

    def __str__(self):

        return f'{self.student.first_name} {self.student.course.name}'
    
    class Meta:

        verbose_name = 'Payments'

        verbose_name_plural ='Payments'

class Transactions(Baseclass):

    payment = models.ForeignKey('Payment',on_delete=models.CASCADE)

    rzp_order_id = models.SlugField()

    amount = models.SlugField()

    status = models.CharField(max_length=20,choices=PaymentStatusChoices.choices,default=PaymentStatusChoices.PENDING)

    transaction_at = models.DateField(null=True)

    rzp_payment = models.SlugField(null=True,blank=True)

    rzp_signature = models.TextField(null=True,blank=True)

    def __str__(self):

        return f'{self.payment.student.first_name} {self.payment.student.course.name}'

    class Meta:

        verbose_name = 'Transactions'

        verbose_name_plural = 'Transactions'


