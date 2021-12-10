from django import forms
from pizza_home.models import *


class OrderStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']

    def __init__(self, *args, **kwargs):
        super(OrderStatusUpdateForm, self).__init__(*args, **kwargs)
        self.fields['status'].widget.attrs['class'] = 'form-control'


class PizzaForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super(PizzaForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['price'].widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['class'] = 'form-control'