from datetime import date
from django import forms
from django.utils.translation import gettext_lazy as _
from pdfcertificate.models import Certificate
from django.forms.widgets import TextInput,Textarea

class DateInput(forms.DateInput):
    input_type = 'date'
    value = date.today()


class CertificateForm(forms.ModelForm):  
    class Meta:  
        model = Certificate
        exclude = ['verification_code']
        widgets = {
            'name': TextInput(attrs={'class': 'input-field ', 'placeholder': 'Name'}),
            'subtitle': Textarea(attrs={'class': 'input-field', 'placeholder':'Subtitle'}),
            'custom_content': Textarea(attrs={'class': 'input-field', 'placeholder':'Custom Content'}),
            'sign': TextInput(attrs={'class': 'input-field', 'placeholder':'Signature'}),
            'date' : DateInput(attrs={'class': 'input-field'})
        }
        error_messages = {
            'name' : {
                'reuired': _("name is a required field")
            },
            'subtitle' : {
                'required': _("subtitle is a required field")
            },
            'date' : {
                'required' : _("date is a required field")
            },
            'sign' : {
                'required' : _("sign is a required field")
            }
        }


class VerifyCertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['verification_code']
        widgets = {
            'verification_code' : TextInput(attrs={'class' : 'input-field','placeholder': 'Enter verification code in the certificate'})
        }