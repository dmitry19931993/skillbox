from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import ValidationError

class UserBioForm(forms.Form):
    name = forms.CharField(max_length= 30)
    age = forms.IntegerField(label='You age', min_value= 5, max_value= 99)
    bio = forms.CharField(label='Biography')

def validate_file_name(file:InMemoryUploadedFile) -> None:
    if file.name and 'virus' in file.name:
        raise ValidationError("В названии файла не должно быть слова 'вирус'")


class UploadFileForm(forms.Form):
    file = forms.FileField(validators=[validate_file_name])
