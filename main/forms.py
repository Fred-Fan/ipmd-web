from django import forms
# -*- coding: utf-8 -*-



class DocumentForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()

#class UploadFileForm(forms.Form):
#    title = forms.CharField(max_length=100)
#    file = forms.ImageField()