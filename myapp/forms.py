from django import forms
from django_countries.fields import CountryField
from localflavor.us.forms import USStateSelect, USZipCodeField


class CheckoutForm(forms.Form):

    f_name = forms.CharField(label='First Name', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    l_name = forms.CharField(label = 'Last Name', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email',max_length=200, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'youremail@example.com'}))
    address = forms.CharField(label='Address',max_length=500, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1234 Main St'}))
    address2 = forms.CharField(label='Address 2', max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apartment or suite'}))
    country = CountryField(blank_label='(select country)').formfield(attrs={
        'class': 'form-control' 
    })
    state = forms.CharField(widget=USStateSelect(), initial='CA')
    zip = USZipCodeField()
