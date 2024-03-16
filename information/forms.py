from django import forms
from information.models import pdf_reader

class UploadFileForm(forms.ModelForm):
    class Meta:
        model=pdf_reader
        fields='__all__'
        
        
        
        