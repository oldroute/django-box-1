# -*- coding: utf-8 -*-
from django import forms
from .models import Unit


class UnitAdminForm(forms.ModelForm):

    class Meta:
        model = Unit
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'large-input'}),
            'email': forms.TextInput(attrs={'class': 'large-input'}),
        }
