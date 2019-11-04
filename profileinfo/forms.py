from django.forms import ModelForm
from .models import post

class contentform(ModelForm):
    class Meta:
        model = post
        fields = ['content']

    def __init__(self, *args, **kwargs):
        super(contentform, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'sap-editable-area ckeditor'

class titleform(ModelForm):
    class Meta:
        model = post
        fields = ['title']

    def __init__(self, *args, **kwargs):
        super(titleform, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'sap-editable-title'