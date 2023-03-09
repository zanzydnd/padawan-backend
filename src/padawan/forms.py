from django import forms


class ImportFileForm(forms.Form):
    file = forms.FileField(label="Файл", allow_empty_file=False)
