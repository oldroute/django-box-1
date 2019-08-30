# -*- coding: utf-8 -*-
from django import forms
from django.core.mail.message import EmailMessage
from feedback.forms import BaseFeedbackForm
from nocaptcha_recaptcha.fields import NoReCaptchaField
from box.units.models import Unit


class BaseForm(BaseFeedbackForm):

    ERROR_MESSAGES = {
        'required': u'Заполните поле',
        'invalid': u'Неправильное значение'
    }

    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].error_messages = self.ERROR_MESSAGES

    captcha = NoReCaptchaField(label='')


class CallForm(BaseForm):

    """ Написать нам """

    def after_mail(self, **kwargs):

        """ Дополнительное письмо в подразделение, указанное в форме """

        recipients = [self.cleaned_data['unit'].email]
        msg = EmailMessage(self.subject, kwargs['message'], self.sender, recipients, headers=kwargs['headers'])
        msg.send()

    company = forms.CharField(
        label=u'Компания',
        widget=forms.TextInput(attrs={'data-set': 1}),
    )
    name = forms.CharField(
        label=u'Ф.И.О.',
        widget=forms.TextInput(attrs={'data-set': 1}),
    )
    email = forms.EmailField(
        label=u'Адрес электронной почты',
        widget=forms.TextInput(attrs={'data-set': 2}),
    )
    phone = forms.CharField(
        label=u'Контактный телефон:', required=False,
        widget=forms.TextInput(attrs={'data-set': 2}),
    )
    unit = forms.ModelChoiceField(
        label=u'Выберите подразделение',
        widget=forms.Select(attrs={'data-set': 3}),
        queryset=Unit.objects.filter(show=True),
        empty_label=''
    )
    message = forms.CharField(
        label=u'Сообщение:', max_length=1000,
        widget=forms.Textarea(attrs={'data-set': 3}),
    )


class CallBackForm(BaseForm):

    """ Обратный звонок """

    def after_mail(self, **kwargs):

        """ Дополнительное письмо в подразделение, указанное в форме """

        recipients = [self.cleaned_data['unit'].email]
        msg = EmailMessage(self.subject, kwargs['message'], self.sender, recipients, headers=kwargs['headers'])
        msg.send()

    company = forms.CharField(
        label=u'Компания',
        widget=forms.TextInput(attrs={'data-set': 1}),
    )

    name = forms.CharField(
        label=u'Ф.И.О.',
        widget=forms.TextInput(attrs={'data-set': 1}),
    )

    phone = forms.CharField(
        label=u'Контактный телефон:', required=False,
        widget=forms.TextInput(attrs={'data-set': 2}),
    )

    unit = forms.ModelChoiceField(
        label=u'Выберите подразделение',
        widget=forms.Select(attrs={'data-set': 2}),
        queryset=Unit.objects.filter(show=True),
        empty_label=''
    )


class ServiceForm(BaseForm):

    """ Заказать услугу """

    company = forms.CharField(
        label=u'Компания',
        widget=forms.TextInput(attrs={'data-set': 1}),
    )
    name = forms.CharField(
        label=u'Ф.И.О.',
        widget=forms.TextInput(attrs={'data-set': 1}),
    )
    email = forms.EmailField(
        label=u'Адрес электронной почты',
        widget=forms.TextInput(attrs={'data-set': 2}),
    )
    phone = forms.CharField(
        label=u'Контактный телефон:', required=False,
        widget=forms.TextInput(attrs={'data-set': 2}),
    )

    message = forms.CharField(
        label=u'Сообщение:', max_length=1000, required=False,
        widget=forms.Textarea(attrs={'data-set': 3}),
    )


class OrderForm(BaseForm):

    """ Заявка на продукцию """

    company = forms.CharField(
        label=u'Компания',
        widget=forms.TextInput(attrs={'data-set': 1}),
    )

    name = forms.CharField(
        label=u'Ф.И.О.',
        widget=forms.TextInput(attrs={'data-set': 1}),
    )
    email = forms.EmailField(
        label=u'Адрес электронной почты',
        widget=forms.TextInput(attrs={'data-set': 2}),
    )
    phone = forms.CharField(
        label=u'Контактный телефон:', required=False,
        widget=forms.TextInput(attrs={'data-set': 2}),
    )
    props = forms.CharField(
        label=u'Параметры / Количество:',
        widget=forms.TextInput(attrs={'data-set': 3}),
    )
    message = forms.CharField(
        label=u'Сообщение:', max_length=1000, required=False,
        widget=forms.Textarea(attrs={'data-set': 3}),
    )
