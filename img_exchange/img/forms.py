from django import forms
from django.forms import ModelForm

from .models import ImagePost

class ImageForm(ModelForm):
    class Meta:
        model = ImagePost
        fields = ['image_1', 'image_2', 'image_3']

        def clean_images(self):
            files = self.cleaned_data['image']
            for file in files:
                if file:
                    if file._size > 15*1024*1024:
                        raise forms.ValidationError("Image file is too large ( > 15mb ).")
                else:
                    raise forms.ValidationError("Could not read the uploaded file.")
                return files