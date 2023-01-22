from dataclasses import field
from tkinter import Widget
from .models import Product, Basket, Order, ImgProduct
from django.forms import ModelForm, Textarea, TextInput, IntegerField

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "price"]
        Widgets = {
            "name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название товара'
            }),
            "description": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Описание товара'
            }),
            "price": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Цена'
            })
        }

