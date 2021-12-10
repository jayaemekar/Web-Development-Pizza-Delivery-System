from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.dispatch import receiver
from django.db.models.signals import post_save 
from accounts.models import CustomUser
from PIL import Image
from io import BytesIO
from channels.layers import get_channel_layer   
from asgiref.sync import async_to_sync
import json
import sys
import string, random 

CHOICES = [
    ('Order Received by Restaurant', 'Order Received by Restaurant'),
    ('Baking', 'Baking'), ('Baked', 'Baked'),
    ('Out for Delivery', 'Out for Delivery'),
    ('Order Received by Customer', 'Order Received by Customer'),
]


class Pizza(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='uploads')
    updated_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Pizza'    
        index_together = ( ('id', 'name') )
    
    def save(self):
        im = Image.open(self.image)    
        im = im.resize( (800,500) )
        output = BytesIO()
        im.save(output, format='JPEG', quality=100)
        output.seek(0)
        self.image = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.image.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)
        super(Pizza,self).save()

    def __str__(self):
        return str(self.name)




class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    order_id = models.CharField(max_length=50, blank=True)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=CHOICES, default='Order Received by Restaurant')
    
    class Meta:
        verbose_name_plural = 'Order'
        ordering = ('-date',)

    @staticmethod
    def get_order_detail(order_id):
        order_case = Order.objects.filter(order_id=order_id).first()
        data = {
            'order_id': order_case.order_id,
            'status': order_case.status,
            'amount': float(order_case.amount),          
        }

        percentage_progress = 0
        if order_case.status == 'Order Received by Restaurant':
            percentage_progress = 20
        elif order_case.status == 'Baking':
            percentage_progress = 40
        elif order_case.status == 'Baked':
            percentage_progress = 60
        elif order_case.status == 'Out for Delivery':
            percentage_progress = 80
        elif order_case.status == 'Order Received by Customer':
            percentage_progress = 100
       
        data['progress'] = percentage_progress 
        return data

    def save(self, *args, **kwargs):
        if not len(self.order_id):
            self.order_id = random_string_generator()
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.order_id)



@receiver(post_save, sender=Order)
def order_status_handler(sender, instance, created, **kwargs):
    if not created:
        data = {
            'order_id': instance.order_id,
            'amount': float(instance.amount), 
            'status': instance.status,
        }

        # Make a progress-percentage based on the 5-types of order-status
        progress_percentage = 0
        if instance.status == 'Order Received by Restaurant':
            progress_percentage = 20
        elif instance.status == 'Baking':
            progress_percentage = 40
        elif instance.status == 'Baked':
            progress_percentage = 60
        elif instance.status == 'Out for Delivery':
            progress_percentage = 80
        elif instance.status == 'Order Received by Customer':
            progress_percentage = 100
        
        data['progress'] = progress_percentage 

        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            'order_%s' % instance.order_id,
            {
                'type': 'order_status',
                'value': json.dumps(data),
            }
        )


def random_string_generator(size=12, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))