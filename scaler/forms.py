from django import forms
from django.core.exceptions import ValidationError


class UploadForm(forms.Form):
    url = forms.URLField(label='Ссылка', required=False)
    image = forms.ImageField(label='Файл', required=False)

    def clean(self):
        url = self.cleaned_data.get('url')
        image = self.cleaned_data.get('image')
        if not url and not image:
            raise ValidationError('Не введено ни одного варианта.')

        if url and image:
            raise ValidationError('Должна быть передана только ссылка или только файл.')


class ResizeForm(forms.Form):
    width = forms.IntegerField(label='Ширина', min_value=10, required=False)
    height = forms.IntegerField(label='Высота', min_value=10, required=False)

    def __init__(self, *args, **kwargs):
        self.image = kwargs.pop('image')
        super().__init__(*args, **kwargs)

    def clean(self):
        width = self.cleaned_data.get('width')
        height = self.cleaned_data.get('height')

        image_ratio = round(self.image.img.width / self.image.img.height, 2)
        if width and height:
            if image_ratio != round(width / height, 2):
                raise ValidationError(
                    'Новые значения должны быть пропорциональны прежним.',
                    'invalid'
                )
