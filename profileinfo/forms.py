from django.forms import ModelForm
from .models import post

class contentform(ModelForm):
    class Meta:
        model = post
        fields = ['content']