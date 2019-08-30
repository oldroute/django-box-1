# -*- coding: utf-8 -*-
from django import forms
from .models import HeroFileItem, HeroFile


class HeroFileItemForm(forms.ModelForm):

    class Meta:
        model = HeroFileItem
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'large-input'}),
            'herofile': forms.Select(attrs={'class': 'large-input'}),
        }


class HeroFileAdminForm(forms.ModelForm):

    class Meta:
        model = HeroFile
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'large-input'}),
            'file': forms.FileInput(attrs={'class': 'large-input'}),
            'overlay_opacity': forms.Select(attrs={'class': 'large-input'}),
        }