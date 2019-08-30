# -*- coding: utf-8 -*-
from django import forms
from .models import Section, Product, Root
from pages.models import Page


class RootAdminForm(forms.ModelForm):

    class Meta:
        model = Root
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'large-input'}),
            'long_title': forms.TextInput(attrs={'class': 'large-input'}),
        }


class ProductAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProductAdminForm, self).__init__(*args, **kwargs)
        ids = [choice[0] for choice in self.fields["produser"].widget.choices]
        pages = Page.objects.filter(id__in=ids[1:])
        self.fields["produser"].widget.choices = [('', u'--- Выберите производителя ---')] + [(s.id, s.title()) for s in pages]

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'large-input'}),
            'slug': forms.TextInput(attrs={'class': 'large-input'}),
            'price': forms.TextInput(attrs={'class': 'large-input'}),
            'vendor_code': forms.TextInput(attrs={'class': 'large-input'}),
            'produser': forms.Select(attrs={'class': 'large-input'}),
        }


class SectionAdminForm(forms.ModelForm):

    class Meta:
        model = Section
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'large-input'}),
            'slug': forms.TextInput(attrs={'class': 'large-input'}),
        }


